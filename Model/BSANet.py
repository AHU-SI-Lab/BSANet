import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torchvision.models import ResNet50_Weights
from torchvision.ops import DeformConv2d

class SEBlock(nn.Module):
    def __init__(self, channel, reduction=16):
        super().__init__()
        self.avg = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y


class StripPooling(nn.Module):
    def __init__(self, ch):
        super().__init__()
        self.pool_h = nn.AdaptiveAvgPool2d((None, 1))
        self.pool_w = nn.AdaptiveAvgPool2d((1, None))
        self.conv = nn.Conv2d(ch, ch, 1, bias=False)
        self.bn = nn.BatchNorm2d(ch)

    def forward(self, x):
        h, w = x.shape[2:]
        x1 = F.interpolate(self.pool_h(x), (h, w), mode="bilinear", align_corners=True)
        x2 = F.interpolate(self.pool_w(x), (h, w), mode="bilinear", align_corners=True)
        return x + torch.sigmoid(self.bn(self.conv(x1 + x2))) * x


class CoordAtt(nn.Module):
    def __init__(self, inp, oup, reduction=32):
        super().__init__()
        self.pool_h = nn.AdaptiveAvgPool2d((None, 1))
        self.pool_w = nn.AdaptiveAvgPool2d((1, None))
        mip = max(8, inp // reduction)

        self.conv1 = nn.Conv2d(inp, mip, 1)
        self.bn1 = nn.BatchNorm2d(mip)
        self.act = nn.Hardswish()

        self.conv_h = nn.Conv2d(mip, oup, 1)
        self.conv_w = nn.Conv2d(mip, oup, 1)

    def forward(self, x):
        n, c, h, w = x.size()

        x_h = self.pool_h(x)
        x_w = self.pool_w(x).permute(0, 1, 3, 2)


        y = torch.cat([x_h, x_w], dim=2)
        y = self.act(self.bn1(self.conv1(y)))


        x_h, x_w = torch.split(y, [h, w], dim=2)
        x_w = x_w.permute(0, 1, 3, 2)

        return x * torch.sigmoid(self.conv_h(x_h)) * torch.sigmoid(self.conv_w(x_w))

class ShapeRefiner_DCN(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch), nn.ReLU(inplace=True)
        )

        self.offset_conv = nn.Conv2d(out_ch, 18, kernel_size=3, padding=1, bias=True)

        self.dcn = DeformConv2d(out_ch, out_ch, kernel_size=3, padding=1)
        self.bn_dcn = nn.BatchNorm2d(out_ch)
        self.relu = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(out_ch, out_ch, 1)

    def forward(self, x):
        x1 = self.conv1(x)
        offset = self.offset_conv(x1)
        x2 = self.dcn(x1, offset)
        x2 = self.relu(self.bn_dcn(x2))
        return self.conv2(x1 + x2)



class FlowAlignmentModule(nn.Module):
    def __init__(self, in_ch):
        super().__init__()
        self.flow_make = nn.Conv2d(in_ch * 2, 2, kernel_size=3, padding=1, bias=False)

    def forward(self, x_high_res, x_low_res):
        x_low_up = F.interpolate(x_low_res, size=x_high_res.shape[2:], mode='bilinear', align_corners=True)
        concat = torch.cat([x_high_res, x_low_up], dim=1)
        flow = self.flow_make(concat)
        return self.flow_warp(x_low_up, flow)

    def flow_warp(self, x, flow):
        B, C, H, W = x.shape
        xx = torch.arange(0, W).view(1, -1).repeat(H, 1).to(x.device)
        yy = torch.arange(0, H).view(-1, 1).repeat(1, W).to(x.device)

        xx = xx.view(1, 1, H, W).repeat(B, 1, 1, 1)
        yy = yy.view(1, 1, H, W).repeat(B, 1, 1, 1)
        grid = torch.cat((xx, yy), 1).float()

        vgrid = grid + flow
        vgrid[:, 0, :, :] = 2.0 * vgrid[:, 0, :, :] / max(W - 1, 1) - 1.0
        vgrid[:, 1, :, :] = 2.0 * vgrid[:, 1, :, :] / max(H - 1, 1) - 1.0
        vgrid = vgrid.permute(0, 2, 3, 1)
        output = F.grid_sample(x, vgrid, mode='bilinear', align_corners=True)
        return output


class AdaptiveFusion_Aligned(nn.Module):
    def __init__(self, chs, out=256):
        super().__init__()
        self.proj = nn.ModuleList([nn.Sequential(
            nn.Conv2d(c, out, 1), nn.BatchNorm2d(out), nn.ReLU(inplace=True)
        ) for c in chs])

        self.fuse = nn.Sequential(
            nn.Conv2d(out * len(chs), out, 3, padding=1),
            nn.BatchNorm2d(out), nn.ReLU(inplace=True)
        )
        self.se = SEBlock(out)
        self.align_modules = nn.ModuleList([
            FlowAlignmentModule(out) for _ in range(len(chs) - 1)
        ])

    def forward(self, xs):
        projs = [layer(x) for layer, x in zip(self.proj, xs)]
        ref = projs[0]
        aligned_feats = [ref]
        for i in range(1, len(projs)):
            aligned = self.align_modules[i - 1](ref, projs[i])
            aligned_feats.append(aligned)
        return self.se(self.fuse(torch.cat(aligned_feats, dim=1)))


class HighFreqEnhancer(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.edge = nn.Sequential(
            nn.Conv2d(in_ch, in_ch, 3, padding=1, groups=in_ch, bias=False),
            nn.Conv2d(in_ch, out_ch, 1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )
        self.ca = CoordAtt(out_ch, out_ch)

    def forward(self, x):
        return self.ca(self.edge(x))

class PPM(nn.Module):
    def __init__(self, in_dim, reduction_dim, bins=(1, 2, 3, 6)):
        super(PPM, self).__init__()
        self.features = []
        for bin in bins:
            self.features.append(nn.Sequential(
                nn.AdaptiveAvgPool2d(bin),
                nn.Conv2d(in_dim, reduction_dim, kernel_size=1, bias=False),
                nn.BatchNorm2d(reduction_dim),
                nn.ReLU(inplace=True)
            ))
        self.features = nn.ModuleList(self.features)

    def forward(self, x):
        x_size = x.size()
        out = [x]
        for f in self.features:
            out.append(F.interpolate(f(x), x_size[2:], mode='bilinear', align_corners=True))
        return torch.cat(out, 1)


class BoundaryAwareFusion(nn.Module):
    def __init__(self, in_ch):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch + 1, in_ch, kernel_size=1, bias=False),
            nn.BatchNorm2d(in_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_ch, in_ch, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(in_ch),
            nn.Sigmoid()
        )

    def forward(self, sem_feat, bnd_prob):
        if bnd_prob.shape[2:] != sem_feat.shape[2:]:
            bnd_prob = F.interpolate(bnd_prob, size=sem_feat.shape[2:], mode='bilinear', align_corners=True)

        cat_feat = torch.cat([sem_feat, bnd_prob], dim=1)
        gate = self.conv(cat_feat)
        return sem_feat + sem_feat * gate

class BSANet(nn.Module):
    def __init__(self, num_classes=2, pretrained=True):
        super().__init__()
        resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1 if pretrained else None)
        self.stem = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu)
        self.pool = resnet.maxpool
        self.l1, self.l2, self.l3, self.l4 = resnet.layer1, resnet.layer2, resnet.layer3, resnet.layer4
        self.sp3 = StripPooling(1024)
        self.ppm = PPM(2048, 512)
        self.sem = AdaptiveFusion_Aligned([256, 512, 1024, 4096])
        self.refiner = ShapeRefiner_DCN(256, 256)
        self.hfe = HighFreqEnhancer(64, 48)
        self.bnd_fuse = nn.Sequential(
            nn.Conv2d(48 + 256, 128, 3, padding=1),
            nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            CoordAtt(128, 128)
        )
        self.bnd_fusion = BoundaryAwareFusion(256)
        self.seg_head = nn.Sequential(
            nn.Conv2d(256, 256, 3, padding=1, bias=False),
            nn.BatchNorm2d(256), nn.ReLU(inplace=True),
            nn.Dropout(0.1),
            nn.Conv2d(256, num_classes, 1)
        )
        self.bnd_head = nn.Conv2d(128, 1, 1)

    def forward(self, x):
        sz = x.shape[2:]
        x0 = self.stem(x)
        c1 = self.l1(self.pool(x0))
        c2 = self.l2(c1)
        c3 = self.l3(c2)
        c4 = self.l4(c3)
        f3 = self.sp3(c3)
        f4 = self.ppm(c4)
        feat_sem = self.sem([c1, c2, f3, f4])
        feat_sem = self.refiner(feat_sem)
        h = self.hfe(x0)
        sem_up = F.interpolate(feat_sem, size=x0.shape[2:], mode="bilinear", align_corners=True)
        feat_bnd = self.bnd_fuse(torch.cat([h, sem_up], dim=1))
        bnd_logits = self.bnd_head(feat_bnd)
        bnd_prob = torch.sigmoid(bnd_logits)
        feat_sem_refined = self.bnd_fusion(feat_sem, bnd_prob)
        seg_logits = self.seg_head(feat_sem_refined)
        if seg_logits.shape[2:] != sz:
            seg_logits = F.interpolate(seg_logits, size=sz, mode="bilinear", align_corners=True)
            bnd_logits = F.interpolate(bnd_logits, size=sz, mode="bilinear", align_corners=True)
        return seg_logits, bnd_logits

def get_model(name, **kwargs):
    return BSANet(**kwargs)