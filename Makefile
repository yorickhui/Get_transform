# Get_transform Makefile
# 提供便捷的构建和开发命令

.PHONY: help install build clean test run dev

# 默认目标：显示帮助
help:
	@echo "==========================================="
	@echo "🌀 Get_transform 构建工具"
	@echo "==========================================="
	@echo ""
	@echo "可用命令:"
	@echo ""
	@echo "  make install      - 安装依赖（创建虚拟环境）"
	@echo "  make build        - 构建可执行文件"
	@echo "  make build-debug  - 构建调试版本"
	@echo "  make clean        - 清理构建文件"
	@echo "  make test         - 运行测试"
	@echo "  make run          - 运行程序（开发模式）"
	@echo "  make dev          - 安装开发依赖"
	@echo "  make dist         - 构建并打包发布"
	@echo ""
	@echo "快速开始:"
	@echo "  1. make install   # 首次安装"
	@echo "  2. make run       # 运行程序"
	@echo "  3. make build     # 构建可执行文件"
	@echo ""

# 安装依赖
install:
	@echo "📦 安装依赖..."
	@./scripts/install.sh

# 构建可执行文件
build:
	@echo "🔨 构建可执行文件..."
	@python3 scripts/build_executable.py --install-pyinstaller

# 构建调试版本
build-debug:
	@echo "🔨 构建调试版本..."
	@python3 scripts/build_executable.py --debug --install-pyinstaller

# 清理构建文件
clean:
	@echo "🧹 清理构建文件..."
	@rm -rf build/ dist/ *.spec
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 清理完成"

# 清理所有（包括虚拟环境）
clean-all: clean
	@echo "🧹 清理虚拟环境..."
	@rm -rf .venv/
	@echo "✅ 完全清理完成"

# 运行测试
test:
	@echo "🧪 运行测试..."
	@if [ -f ".venv/bin/activate" ]; then \
		. .venv/bin/activate && python Get_transform/test_cross_platform.py; \
	else \
		python3 Get_transform/test_cross_platform.py; \
	fi

# 运行程序（开发模式）
run:
	@echo "🚀 启动程序..."
	@if [ -f ".venv/bin/activate" ]; then \
		. .venv/bin/activate && python Get_transform/launch.py; \
	else \
		python3 Get_transform/launch.py; \
	fi

# 安装开发依赖
dev:
	@echo "🛠️  安装开发依赖..."
	@python3 -m pip install --upgrade pip
	@python3 -m pip install -r Get_transform/requirements.txt
	@python3 -m pip install pyinstaller pytest black flake8
	@echo "✅ 开发环境配置完成"

# 构建并打包发布
dist: clean build
	@echo "📦 打包发布版本..."
	@mkdir -p release
	@if [ -f "dist/get_transform" ]; then \
		cp dist/get_transform release/; \
		cp README.md release/; \
		echo "✅ 发布包已创建在 release/ 目录"; \
	else \
		echo "❌ 构建失败，无法创建发布包"; \
		exit 1; \
	fi

# 格式化代码
format:
	@echo "🎨 格式化代码..."
	@python3 -m black Get_transform/*.py
	@echo "✅ 格式化完成"

# 代码检查
lint:
	@echo "🔍 代码检查..."
	@python3 -m flake8 Get_transform/*.py --max-line-length=120 --extend-ignore=E203,W503
	@echo "✅ 检查完成"
