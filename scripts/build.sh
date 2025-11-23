#!/bin/bash
# Get_transform 构建脚本 (Linux/macOS)
# 用法: ./scripts/build.sh [选项]

set -e  # 出错时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
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

echo "=========================================="
echo "🌀 Get_transform 构建工具"
echo "=========================================="
print_info "项目目录: $PROJECT_ROOT"
print_info "平台: $(uname -s) $(uname -m)"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 未安装"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
print_success "Python: $PYTHON_VERSION"

# 进入项目目录
cd "$PROJECT_ROOT"

# 解析命令行参数
CLEAN=false
DEBUG=false
TEST=false
INSTALL_DEPS=false

for arg in "$@"; do
    case $arg in
        --clean)
            CLEAN=true
            shift
            ;;
        --debug)
            DEBUG=true
            shift
            ;;
        --test)
            TEST=true
            shift
            ;;
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --help)
            echo ""
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --clean         清理构建目录"
            echo "  --debug         启用调试模式"
            echo "  --test          构建后测试"
            echo "  --install-deps  安装依赖包"
            echo "  --help          显示此帮助信息"
            echo ""
            exit 0
            ;;
    esac
done

# 安装依赖（如果需要）
if [ "$INSTALL_DEPS" = true ]; then
    print_info "安装依赖包..."
    python3 -m pip install -r Get_transform/requirements.txt
    python3 -m pip install pyinstaller
    print_success "依赖安装完成"
fi

# 构建参数
BUILD_ARGS=""
if [ "$CLEAN" = true ]; then
    BUILD_ARGS="$BUILD_ARGS --clean"
fi
if [ "$DEBUG" = true ]; then
    BUILD_ARGS="$BUILD_ARGS --debug"
fi
if [ "$TEST" = true ]; then
    BUILD_ARGS="$BUILD_ARGS --test"
fi

# 运行构建脚本
print_info "开始构建..."
python3 scripts/build_executable.py $BUILD_ARGS

# 检查构建结果
if [ -f "dist/get_transform" ]; then
    print_success "构建成功！"
    echo ""
    echo "可执行文件位置: dist/get_transform"
    echo "文件大小: $(du -h dist/get_transform | cut -f1)"
    echo ""
    echo "使用方法: ./dist/get_transform"
else
    print_error "构建失败：未找到可执行文件"
    exit 1
fi

echo "=========================================="
print_success "构建完成"
echo "=========================================="
