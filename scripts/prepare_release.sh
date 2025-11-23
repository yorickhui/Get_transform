#!/bin/bash
# Get_transform 发布准备脚本
# 用于准备新版本发布

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}\n"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 获取脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

print_header "🌀 Get_transform 发布准备向导"

print_info "项目目录: $PROJECT_ROOT"
print_info "平台: $(uname -s) $(uname -m)"

cd "$PROJECT_ROOT"

# 1. 检查 Git 状态
print_header "1️⃣  检查 Git 状态"

if [ -n "$(git status --porcelain)" ]; then
    print_warning "工作目录有未提交的更改"
    git status --short
    echo ""
    read -p "是否继续? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消"
        exit 0
    fi
else
    print_success "工作目录干净"
fi

# 2. 询问版本号
print_header "2️⃣  版本信息"

CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
print_info "当前版本: $CURRENT_VERSION"

read -p "请输入新版本号 (例如: v1.0.1): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    print_error "版本号不能为空"
    exit 1
fi

# 确保版本号以 v 开头
if [[ ! $NEW_VERSION =~ ^v ]]; then
    NEW_VERSION="v$NEW_VERSION"
fi

print_info "新版本号: $NEW_VERSION"

# 3. 运行测试
print_header "3️⃣  运行测试"

if [ -f "Get_transform/test_cross_platform.py" ]; then
    print_info "运行测试套件..."
    if python3 Get_transform/test_cross_platform.py; then
        print_success "测试通过"
    else
        print_error "测试失败"
        exit 1
    fi
else
    print_warning "未找到测试文件，跳过"
fi

# 4. 构建可执行文件
print_header "4️⃣  构建可执行文件"

read -p "是否构建可执行文件? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "开始构建..."
    
    # 清理旧的构建
    make clean
    
    # 构建
    if python3 scripts/build_executable.py --install-pyinstaller; then
        print_success "构建成功"
        
        # 显示文件信息
        if [ -f "dist/get_transform" ]; then
            SIZE=$(du -h dist/get_transform | cut -f1)
            print_info "可执行文件: dist/get_transform"
            print_info "文件大小: $SIZE"
        fi
    else
        print_error "构建失败"
        exit 1
    fi
fi

# 5. 创建发布目录
print_header "5️⃣  准备发布包"

RELEASE_DIR="release-$NEW_VERSION"
if [ -d "$RELEASE_DIR" ]; then
    print_warning "发布目录已存在: $RELEASE_DIR"
    rm -rf "$RELEASE_DIR"
fi

mkdir -p "$RELEASE_DIR"
print_success "创建发布目录: $RELEASE_DIR"

# 复制文件
if [ -f "dist/get_transform" ]; then
    PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    EXECUTABLE_NAME="get_transform-${NEW_VERSION}-${PLATFORM}-${ARCH}"
    
    cp "dist/get_transform" "$RELEASE_DIR/$EXECUTABLE_NAME"
    print_success "复制可执行文件: $EXECUTABLE_NAME"
    
    # 生成 SHA256
    (cd "$RELEASE_DIR" && sha256sum "$EXECUTABLE_NAME" > "$EXECUTABLE_NAME.sha256")
    print_success "生成 SHA256 校验和"
fi

# 复制文档
cp README.md "$RELEASE_DIR/"
cp BUILD.md "$RELEASE_DIR/"
cp QUICKSTART.md "$RELEASE_DIR/"
cp CHANGELOG.md "$RELEASE_DIR/"
print_success "复制文档文件"

# 6. 更新 CHANGELOG
print_header "6️⃣  更新 CHANGELOG"

print_info "请在 CHANGELOG.md 中更新版本信息"
print_info "将 [Unreleased] 改为 [$NEW_VERSION] - $(date +%Y-%m-%d)"

read -p "是否现在编辑 CHANGELOG? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ${EDITOR:-nano} CHANGELOG.md
fi

# 7. 生成发布说明
print_header "7️⃣  生成发布说明"

RELEASE_NOTES="$RELEASE_DIR/RELEASE_NOTES.md"
cat > "$RELEASE_NOTES" << EOF
# Get_transform $NEW_VERSION

## 🎉 新版本发布

**发布日期**: $(date +%Y-%m-%d)

## 📦 下载

根据你的操作系统下载对应的文件：

### Linux
- 文件名: \`get_transform-${NEW_VERSION}-linux-${ARCH}\`
- 运行方式: \`chmod +x get_transform-${NEW_VERSION}-linux-${ARCH} && ./get_transform-${NEW_VERSION}-linux-${ARCH}\`

### macOS
- 构建说明: 请在 macOS 系统上运行 \`make build\` 构建

### Windows
- 构建说明: 请在 Windows 系统上运行 \`.\scripts\build.ps1 -InstallDeps\` 构建

## 🚀 快速开始

1. 下载对应平台的可执行文件
2. 运行程序（首次运行会引导配置）
3. 将 GET笔记 导出的文件放入 \`history/\` 目录
4. 按照菜单提示操作

详细使用说明请查看 [QUICKSTART.md](QUICKSTART.md)。

## 📋 更新内容

$(grep -A 20 "## \[Unreleased\]" CHANGELOG.md | tail -n +2 | head -n 20)

完整更新日志请查看 [CHANGELOG.md](CHANGELOG.md)。

## 🔒 校验和

下载后请验证文件完整性：

\`\`\`bash
sha256sum -c get_transform-${NEW_VERSION}-*.sha256
\`\`\`

## 📚 文档

- [README.md](README.md) - 项目介绍和功能说明
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南（非技术用户）
- [BUILD.md](BUILD.md) - 构建说明（开发者）
- [CHANGELOG.md](CHANGELOG.md) - 完整更新日志

## ❓ 问题反馈

如果遇到问题，请在 [Issues](https://github.com/yorickhui/Get_transform/issues) 中反馈。

---

**感谢使用 Get_transform！** ⭐
EOF

print_success "生成发布说明: $RELEASE_NOTES"

# 8. 显示发布检查清单
print_header "8️⃣  发布检查清单"

echo "在发布前，请确认："
echo ""
echo "  [ ] 所有测试通过"
echo "  [ ] 文档已更新"
echo "  [ ] CHANGELOG 已更新"
echo "  [ ] 版本号正确"
echo "  [ ] 在所有平台上构建并测试"
echo "  [ ] 可执行文件可以正常运行"
echo "  [ ] 配置功能正常工作"
echo "  [ ] 文件操作功能正常工作"
echo ""

# 9. Git 操作
print_header "9️⃣  Git 操作"

read -p "是否提交更改并创建标签? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "提交更改..."
    git add -A
    git commit -m "Release $NEW_VERSION"
    
    print_info "创建标签..."
    git tag -a "$NEW_VERSION" -m "Version $NEW_VERSION"
    
    print_success "已创建标签: $NEW_VERSION"
    
    read -p "是否推送到远程仓库? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin main
        git push origin "$NEW_VERSION"
        print_success "已推送到远程仓库"
    fi
fi

# 10. 完成
print_header "✅ 发布准备完成"

echo "发布包位置: $RELEASE_DIR"
echo ""
echo "下一步:"
echo "  1. 在 Windows 上构建可执行文件"
echo "  2. 在 macOS 上构建可执行文件"
echo "  3. 将所有平台的可执行文件添加到发布包"
echo "  4. 在 GitHub 上创建 Release"
echo "  5. 上传所有文件到 Release"
echo "  6. 复制 RELEASE_NOTES.md 的内容到 Release 说明"
echo ""
echo "GitHub Release 页面:"
echo "  https://github.com/yorickhui/Get_transform/releases/new?tag=$NEW_VERSION"
echo ""

print_success "发布准备完成！"
