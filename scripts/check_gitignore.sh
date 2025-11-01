#!/bin/bash

# Git 提交前的 .gitignore 检查脚本
# 用途：确保敏感文件不会被提交到 GitHub

#set -e  # 遇到错误立即退出

echo ""
echo "🔍 ====================================="
echo "   Git 提交前安全检查"
echo "====================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查计数
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# 检查函数
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# ========================================
# 检查 1: .gitignore 文件存在
# ========================================
echo "📋 检查 1: .gitignore 文件"
if [ -f .gitignore ]; then
    check_pass ".gitignore 文件存在"
else
    check_fail ".gitignore 文件不存在！"
    exit 1
fi

# ========================================
# 检查 2: 敏感文件是否被追踪
# ========================================
echo ""
echo "🔐 检查 2: 敏感文件（环境变量）"

SENSITIVE_FILES=$(git ls-files | grep -E "^\.env$|\.env\.local$" || true)
if [ -z "$SENSITIVE_FILES" ]; then
    check_pass "环境变量文件未被追踪"
else
    check_fail "发现敏感文件被追踪："
    echo "$SENSITIVE_FILES"
    echo "   解决方法: git rm --cached .env"
fi

# ========================================
# 检查 3: 虚拟环境文件夹
# ========================================
echo ""
echo "🐍 检查 3: Python 虚拟环境"

VENV_FILES=$(git ls-files | grep -E "^\.venv/|^venv/|^ENV/" || true)
if [ -z "$VENV_FILES" ]; then
    check_pass "虚拟环境未被追踪"
else
    check_fail "发现虚拟环境被追踪"
    echo "   文件数量: $(echo "$VENV_FILES" | wc -l)"
    echo "   解决方法: git rm -r --cached .venv"
fi

# ========================================
# 检查 4: Python 缓存文件
# ========================================
echo ""
echo "📦 检查 4: Python 缓存文件"

PYCACHE_FILES=$(git ls-files | grep -E "__pycache__/|\.pyc$|\.pyo$" || true)
if [ -z "$PYCACHE_FILES" ]; then
    check_pass "Python 缓存未被追踪"
else
    check_fail "发现缓存文件被追踪"
    echo "   文件数量: $(echo "$PYCACHE_FILES" | wc -l)"
    echo "   解决方法: git rm -r --cached __pycache__"
fi

# ========================================
# 检查 5: IDE 配置文件
# ========================================
echo ""
echo "💻 检查 5: IDE 配置文件"

IDE_FILES=$(git ls-files | grep -E "^\.idea/|^\.vscode/|\.iml$" || true)
if [ -z "$IDE_FILES" ]; then
    check_pass "IDE 配置未被追踪"
else
    check_fail "发现 IDE 配置被追踪"
    echo "   文件数量: $(echo "$IDE_FILES" | wc -l)"
    echo "   解决方法: git rm -r --cached .idea .vscode"
fi

# ========================================
# 检查 6: 系统文件
# ========================================
echo ""
echo "🖥️  检查 6: 系统文件"

SYS_FILES=$(git ls-files | grep -E "\.DS_Store$" || true)
if [ -z "$SYS_FILES" ]; then
    check_pass "系统文件未被追踪"
else
    check_fail "发现系统文件被追踪"
    echo "   解决方法: git rm --cached .DS_Store"
fi

# ========================================
# 检查 7: 数据文件
# ========================================
echo ""
echo "📁 检查 7: 数据文件"

DATA_FILES=$(git ls-files | grep -E "^data/" || true)
if [ -z "$DATA_FILES" ]; then
    check_pass "数据文件未被追踪"
else
    check_warn "发现数据文件被追踪（可能需要检查）"
    echo "   文件数量: $(echo "$DATA_FILES" | wc -l)"
    echo "   如果不应该提交: git rm -r --cached data"
fi

# ========================================
# 检查 8: 备份文件
# ========================================
echo ""
echo "💾 检查 8: 备份文件"

BACKUP_FILES=$(git ls-files | grep -E "\.old$|\.backup$|\.bak$" || true)
if [ -z "$BACKUP_FILES" ]; then
    check_pass "备份文件未被追踪"
else
    check_fail "发现备份文件被追踪"
    echo "$BACKUP_FILES"
    echo "   解决方法: git rm --cached *.old"
fi

# ========================================
# 检查 9: 测试缓存
# ========================================
echo ""
echo "🧪 检查 9: 测试缓存"

TEST_CACHE=$(git ls-files | grep -E "\.pytest_cache/|\.coverage" || true)
if [ -z "$TEST_CACHE" ]; then
    check_pass "测试缓存未被追踪"
else
    check_fail "发现测试缓存被追踪"
    echo "   解决方法: git rm -r --cached .pytest_cache"
fi

# ========================================
# 检查 10: .gitignore 规则完整性
# ========================================
echo ""
echo "📝 检查 10: .gitignore 规则完整性"

REQUIRED_RULES=(".venv/" "__pycache__/" ".env" ".idea/" "*.old" "data/")
MISSING_RULES=()

for rule in "${REQUIRED_RULES[@]}"; do
    if grep -q "$rule" .gitignore; then
        :  # 规则存在，不做任何事
    else
        MISSING_RULES+=("$rule")
    fi
done

if [ ${#MISSING_RULES[@]} -eq 0 ]; then
    check_pass ".gitignore 规则完整"
else
    check_warn ".gitignore 缺少以下规则："
    for rule in "${MISSING_RULES[@]}"; do
        echo "   - $rule"
    done
fi

# ========================================
# 总结
# ========================================
echo ""
echo "====================================="
echo "📊 检查总结"
echo "====================================="
echo -e "总计: ${TOTAL_CHECKS} 项检查"
echo -e "${GREEN}通过: ${PASSED_CHECKS}${NC}"
echo -e "${RED}失败: ${FAILED_CHECKS}${NC}"
echo ""

if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}🎉 所有检查通过！可以安全提交到 GitHub！${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  发现 ${FAILED_CHECKS} 个问题，请先修复再提交！${NC}"
    echo ""
    echo "💡 快速修复命令："
    echo "   git rm --cached <文件名>     # 移除单个文件"
    echo "   git rm -r --cached <文件夹>  # 移除文件夹"
    echo ""
    exit 1
fi