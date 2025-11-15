#!/bin/bash

# Git 提交前的 .gitignore 检查脚本
# 用途：确保敏感文件不会被提交到 GitHub
# 更新：Day 2 - 添加前端（Next.js）检查项

echo ""
echo "🔍 ====================================="
echo "   Git 提交前安全检查 (Full-Stack版)"
echo "====================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查计数
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNED_CHECKS=0

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
    ((WARNED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ========================================
# 检查 1: .gitignore 文件存在
# ========================================
echo "📋 检查 1: .gitignore 文件"
if [ -f .gitignore ]; then
    check_pass ".gitignore 文件存在"
else
    check_fail ".gitignore 文件不存在！"
    echo "   解决方法: 创建 .gitignore 文件"
    exit 1
fi

# ========================================
# 后端检查 (Python/FastAPI)
# ========================================
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  后端 (Python/FastAPI) 检查${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"

# 检查 2: 敏感文件（环境变量）
echo ""
echo "🔐 检查 2: 敏感文件（环境变量）"

SENSITIVE_FILES=$(git ls-files | grep -E "^\.env$|\.env\.local$|\.env\.production$" || true)
if [ -z "$SENSITIVE_FILES" ]; then
    check_pass "环境变量文件未被追踪"
else
    check_fail "发现敏感文件被追踪："
    echo "$SENSITIVE_FILES"
    echo "   解决方法: git rm --cached .env"
fi

# 检查 3: Python 虚拟环境
echo ""
echo "🐍 检查 3: Python 虚拟环境"

VENV_FILES=$(git ls-files | grep -E "^\.venv/|^venv/|^ENV/|^env/" || true)
if [ -z "$VENV_FILES" ]; then
    check_pass "虚拟环境未被追踪"
else
    check_fail "发现虚拟环境被追踪"
    echo "   文件数量: $(echo "$VENV_FILES" | wc -l | xargs)"
    echo "   解决方法: git rm -r --cached .venv"
fi

# 检查 4: Python 缓存文件
echo ""
echo "📦 检查 4: Python 缓存文件"

PYCACHE_FILES=$(git ls-files | grep -E "__pycache__/|\.pyc$|\.pyo$|\.pyd$" || true)
if [ -z "$PYCACHE_FILES" ]; then
    check_pass "Python 缓存未被追踪"
else
    check_fail "发现缓存文件被追踪"
    echo "   文件数量: $(echo "$PYCACHE_FILES" | wc -l | xargs)"
    echo "   解决方法: git rm -r --cached **/__pycache__"
fi

# 检查 5: 测试缓存
echo ""
echo "🧪 检查 5: 测试缓存"

TEST_CACHE=$(git ls-files | grep -E "\.pytest_cache/|\.coverage|htmlcov/" || true)
if [ -z "$TEST_CACHE" ]; then
    check_pass "测试缓存未被追踪"
else
    check_fail "发现测试缓存被追踪"
    echo "   解决方法: git rm -r --cached .pytest_cache .coverage htmlcov"
fi

# 检查 6: 数据库文件
echo ""
echo "💾 检查 6: 数据库文件"

DB_FILES=$(git ls-files | grep -E "\.db$|\.sqlite$|\.sqlite3$" || true)
if [ -z "$DB_FILES" ]; then
    check_pass "数据库文件未被追踪"
else
    check_warn "发现数据库文件被追踪（通常不应提交）"
    echo "$DB_FILES"
    echo "   如果不应该提交: git rm --cached *.db"
fi

# ========================================
# 前端检查 (Next.js/React)
# ========================================
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  前端 (Next.js/React) 检查${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"

# 检查 7: node_modules
echo ""
echo "📦 检查 7: node_modules 目录"

NODE_MODULES=$(git ls-files | grep -E "node_modules/" || true)
if [ -z "$NODE_MODULES" ]; then
    check_pass "node_modules 未被追踪"
else
    check_fail "发现 node_modules 被追踪（这会导致仓库巨大！）"
    echo "   文件数量: $(echo "$NODE_MODULES" | wc -l | xargs)"
    echo "   解决方法: git rm -r --cached frontend/node_modules"
fi

# 检查 8: Next.js 编译文件
echo ""
echo "⚡ 检查 8: Next.js 编译文件"

NEXT_BUILD=$(git ls-files | grep -E "\.next/|out/" || true)
if [ -z "$NEXT_BUILD" ]; then
    check_pass "Next.js 编译文件未被追踪"
else
    check_fail "发现 Next.js 编译文件被追踪"
    echo "   文件数量: $(echo "$NEXT_BUILD" | wc -l | xargs)"
    echo "   解决方法: git rm -r --cached frontend/.next frontend/out"
fi

# 检查 9: 前端环境变量
echo ""
echo "🔐 检查 9: 前端环境变量"

FRONTEND_ENV=$(git ls-files | grep -E "frontend/\.env\.local|frontend/\.env\.development\.local|frontend/\.env\.production\.local" || true)
if [ -z "$FRONTEND_ENV" ]; then
    check_pass "前端环境变量未被追踪"
else
    check_fail "发现前端环境变量被追踪"
    echo "$FRONTEND_ENV"
    echo "   解决方法: git rm --cached frontend/.env.local"
fi

# 检查 10: package-lock.json / yarn.lock
echo ""
echo "🔒 检查 10: 包管理器锁文件"

LOCK_FILES=$(git ls-files | grep -E "package-lock\.json$|yarn\.lock$" || true)
if [ -n "$LOCK_FILES" ]; then
    check_pass "锁文件已追踪（正确）"
else
    check_warn "未找到 package-lock.json 或 yarn.lock"
    echo "   建议: 这些文件应该被提交以确保依赖版本一致"
fi

# ========================================
# 通用检查
# ========================================
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  通用检查${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"

# 检查 11: IDE 配置文件
echo ""
echo "💻 检查 11: IDE 配置文件"

IDE_FILES=$(git ls-files | grep -E "^\.idea/|^\.vscode/|\.iml$" || true)
if [ -z "$IDE_FILES" ]; then
    check_pass "IDE 配置未被追踪"
else
    check_fail "发现 IDE 配置被追踪"
    echo "   文件数量: $(echo "$IDE_FILES" | wc -l | xargs)"
    echo "   解决方法: git rm -r --cached .idea .vscode"
fi

# 检查 12: 系统文件
echo ""
echo "🖥️  检查 12: 系统文件"

SYS_FILES=$(git ls-files | grep -E "\.DS_Store$|Thumbs\.db$|desktop\.ini$" || true)
if [ -z "$SYS_FILES" ]; then
    check_pass "系统文件未被追踪"
else
    check_fail "发现系统文件被追踪"
    echo "$SYS_FILES"
    echo "   解决方法: git rm --cached .DS_Store"
fi

# 检查 13: 数据文件夹
echo ""
echo "📁 检查 13: 数据文件夹"

DATA_FILES=$(git ls-files | grep -E "^data/" || true)
if [ -z "$DATA_FILES" ]; then
    check_pass "数据文件未被追踪"
else
    check_warn "发现数据文件被追踪（请确认是否需要）"
    echo "   文件数量: $(echo "$DATA_FILES" | wc -l | xargs)"
    echo "   如果不应该提交: git rm -r --cached data"
fi

# 检查 14: 备份文件
echo ""
echo "💾 检查 14: 备份文件"

BACKUP_FILES=$(git ls-files | grep -E "\.old$|\.backup$|\.bak$|\.swp$|~$" || true)
if [ -z "$BACKUP_FILES" ]; then
    check_pass "备份文件未被追踪"
else
    check_fail "发现备份文件被追踪"
    echo "$BACKUP_FILES"
    echo "   解决方法: git rm --cached *.old *.backup"
fi

# 检查 15: 日志文件
echo ""
echo "📝 检查 15: 日志文件"

LOG_FILES=$(git ls-files | grep -E "\.log$|logs/" || true)
if [ -z "$LOG_FILES" ]; then
    check_pass "日志文件未被追踪"
else
    check_warn "发现日志文件被追踪"
    echo "$LOG_FILES"
    echo "   如果不应该提交: git rm --cached *.log"
fi

# ========================================
# 检查 16: .gitignore 规则完整性
# ========================================
echo ""
echo "📝 检查 16: .gitignore 规则完整性"

REQUIRED_RULES=(
    "# Python"
    ".venv/"
    "__pycache__/"
    "*.pyc"
    ".env"
    ".pytest_cache"
    "# Frontend"
    "node_modules/"
    ".next/"
    "frontend/.env.local"
    "# IDE"
    ".idea/"
    ".vscode/"
    "# System"
    ".DS_Store"
    "# Data & Logs"
    "data/"
    "*.log"
    "# Backup"
    "*.old"
    "*.backup"
)

MISSING_RULES=()

for rule in "${REQUIRED_RULES[@]}"; do
    # 跳过注释行的检查
    if [[ $rule == \#* ]]; then
        continue
    fi
    
    if grep -qF "$rule" .gitignore 2>/dev/null; then
        :  # 规则存在，不做任何事
    else
        MISSING_RULES+=("$rule")
    fi
done

if [ ${#MISSING_RULES[@]} -eq 0 ]; then
    check_pass ".gitignore 规则完整"
else
    check_warn ".gitignore 建议添加以下规则："
    for rule in "${MISSING_RULES[@]}"; do
        echo "   - $rule"
    done
    echo ""
    echo "   💡 快速添加所有缺失规则："
    echo "   cat >> .gitignore << 'EOF'"
    for rule in "${MISSING_RULES[@]}"; do
        echo "$rule"
    done
    echo "EOF"
fi

# ========================================
# 检查 17: 大文件检查
# ========================================
echo ""
echo "📏 检查 17: 大文件检查（>10MB）"

LARGE_FILES=$(git ls-files | xargs -I {} sh -c 'if [ -f "{}" ]; then size=$(stat -f%z "{}" 2>/dev/null || stat -c%s "{}" 2>/dev/null); if [ "$size" -gt 10485760 ]; then echo "{} ($(echo "scale=2; $size/1048576" | bc)MB)"; fi; fi' || true)

if [ -z "$LARGE_FILES" ]; then
    check_pass "未发现大文件"
else
    check_warn "发现大文件（>10MB）："
    echo "$LARGE_FILES"
    echo "   建议: 使用 Git LFS 管理大文件"
fi

# ========================================
# 总结
# ========================================
echo ""
echo "====================================="
echo "📊 检查总结"
echo "====================================="
echo -e "总计: ${TOTAL_CHECKS} 项检查"
echo -e "${GREEN}✅ 通过: ${PASSED_CHECKS}${NC}"
echo -e "${YELLOW}⚠️  警告: ${WARNED_CHECKS}${NC}"
echo -e "${RED}❌ 失败: ${FAILED_CHECKS}${NC}"
echo ""

# 提供详细的修复建议
if [ $FAILED_CHECKS -gt 0 ]; then
    echo -e "${RED}⚠️  发现 ${FAILED_CHECKS} 个问题，建议修复后再提交！${NC}"
    echo ""
    echo "💡 常用修复命令："
    echo ""
    echo "   # 移除单个文件"
    echo "   git rm --cached <文件名>"
    echo ""
    echo "   # 移除文件夹"
    echo "   git rm -r --cached <文件夹>"
    echo ""
    echo "   # 移除所有 .pyc 文件"
    echo "   git rm --cached \$(git ls-files | grep '\.pyc$')"
    echo ""
    echo "   # 移除 node_modules"
    echo "   git rm -r --cached frontend/node_modules"
    echo ""
    echo "   # 移除 .next 编译文件"
    echo "   git rm -r --cached frontend/.next"
    echo ""
    echo "   # 批量操作后需要提交"
    echo "   git commit -m 'chore: update .gitignore and remove tracked files'"
    echo ""
fi

if [ $WARNED_CHECKS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  有 ${WARNED_CHECKS} 个警告，请检查是否需要处理${NC}"
    echo ""
fi

if [ $FAILED_CHECKS -eq 0 ] && [ $WARNED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}🎉 完美！所有检查通过，可以安全提交到 GitHub！${NC}"
    echo ""
    echo "📤 建议的提交命令："
    echo "   git add ."
    echo "   git commit -m 'feat: your commit message'"
    echo "   git push origin main"
    echo ""
    exit 0
elif [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✅ 主要检查通过，但有一些警告${NC}"
    echo -e "${YELLOW}   建议检查警告项后再提交${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}❌ 请先修复上述问题再提交！${NC}"
    echo ""
    exit 1
fi
