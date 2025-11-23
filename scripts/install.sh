#!/bin/bash
# Get_transform 安装脚本 (Linux/macOS)
# 自动创建虚拟环境并安装依赖

set -e  # 出错时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
echo "🌀 Get_transform 安装向导"
echo "=========================================="
print_info "项目目录: $PROJECT_ROOT"
print_info "平台: $(uname -s)"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 未安装"
    print_info "请从 https://www.python.org 下载安装 Python 3.6+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
print_success "Python: $PYTHON_VERSION"

# 进入项目目录
cd "$PROJECT_ROOT"

# 检查虚拟环境是否已存在
if [ -d ".venv" ]; then
    print_warning "虚拟环境已存在"
    read -p "是否删除并重新创建? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "删除旧的虚拟环境..."
        rm -rf .venv
    else
        print_info "使用现有虚拟环境"
    fi
fi

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    print_info "创建虚拟环境..."
    python3 -m venv .venv
    print_success "虚拟环境创建成功"
fi

# 激活虚拟环境
print_info "激活虚拟环境..."
source .venv/bin/activate

# 升级 pip
print_info "升级 pip..."
python -m pip install --upgrade pip

# 安装依赖
print_info "安装项目依赖..."
if [ -f "Get_transform/requirements.txt" ]; then
    pip install -r Get_transform/requirements.txt
    print_success "依赖安装完成"
else
    print_warning "未找到 requirements.txt"
fi

# 创建启动脚本
print_info "创建启动脚本..."
cat > run.sh << 'EOF'
#!/bin/bash
# Get_transform 启动脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source .venv/bin/activate

# 运行程序
python Get_transform/launch.py

# 退出时暂停
read -p "按回车键退出..."
EOF

chmod +x run.sh
print_success "启动脚本创建成功: run.sh"

echo ""
echo "=========================================="
print_success "安装完成！"
echo "=========================================="
echo ""
echo "📖 使用方法:"
echo ""
echo "1. 运行程序（推荐）:"
echo "   ./run.sh"
echo ""
echo "2. 手动运行:"
echo "   source .venv/bin/activate"
echo "   python Get_transform/launch.py"
echo ""
echo "3. 构建可执行文件:"
echo "   ./scripts/build.sh --install-deps"
echo ""
print_info "首次运行会引导你配置导出路径"
print_info "详细文档请查看 README.md"
echo ""
