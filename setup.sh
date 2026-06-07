#!/usr/bin/env bash
# jobbi setup — installs JobSpy MCP server and configures Claude Code
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

REPO_URL="https://github.com/chinpeerapat/jobspy-mcp-server.git"
INSTALL_DIR="$HOME/tools/jobspy-mcp-server"
VENV="$INSTALL_DIR/.venv"

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
fail() { echo -e "${RED}✗${NC} $1"; exit 1; }

echo ""
echo -e "${BOLD}jobbi — JobSpy MCP Setup${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── OS check ──────────────────────────────────────────────────────────────────
if [[ "${OSTYPE:-}" == "msys" || "${OSTYPE:-}" == "win32" || "${OSTYPE:-}" == "cygwin" ]]; then
    fail "Windows detected. Please run this script inside WSL or Git Bash."
fi

# ── Prerequisites ──────────────────────────────────────────────────────────────
echo "Checking prerequisites..."

command -v git &>/dev/null || fail "git not found. Install git and try again."
ok "git"

if ! command -v uv &>/dev/null; then
    warn "uv not found — installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    command -v uv &>/dev/null || fail "uv installation failed. Install manually: https://docs.astral.sh/uv/"
fi
ok "uv $(uv --version | awk '{print $2}')"

echo ""

# ── Clone / update repo ────────────────────────────────────────────────────────
echo "Setting up JobSpy MCP server..."

if [ -d "$INSTALL_DIR/.git" ]; then
    warn "Already installed — pulling latest updates..."
    git -C "$INSTALL_DIR" pull --quiet
else
    git clone --quiet "$REPO_URL" "$INSTALL_DIR"
fi
ok "repository at $INSTALL_DIR"

# ── Create venv and install deps ───────────────────────────────────────────────
echo "Creating Python environment (may download Python if needed)..."
uv venv "$VENV" --python 3.12 --quiet 2>/dev/null \
    || uv venv "$VENV" --clear --quiet 2>/dev/null \
    || fail "Failed to create virtual environment at $VENV"
[ -f "$VENV/bin/python" ] || fail "Virtual environment created but Python not found at $VENV/bin/python"
uv pip install --quiet --python "$VENV/bin/python" \
    mcp fastmcp python-jobspy pandas pydantic
ok "dependencies installed"

echo ""

# ── Verify server.py exists ────────────────────────────────────────────────────
SERVER_PY="$INSTALL_DIR/jobspy_mcp_server/server.py"
[ -f "$SERVER_PY" ] || fail "server.py not found at $SERVER_PY — clone may be incomplete"

# ── Smoke test: server starts without crashing ─────────────────────────────────
echo "Verifying server starts correctly..."
"$VENV/bin/python" "$SERVER_PY" &
SERVER_PID=$!
sleep 2
if kill -0 $SERVER_PID 2>/dev/null; then
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
    ok "server starts cleanly"
else
    fail "server exited immediately — check $SERVER_PY for errors"
fi

# ── Register with Claude Code via claude mcp add ───────────────────────────────
echo "Registering MCP server with Claude Code..."

if ! command -v claude &>/dev/null; then
    fail "claude CLI not found. Install Claude Code first: https://claude.ai/code"
fi

# Remove any stale entry (ignore errors if it doesn't exist)
claude mcp remove jobspy -s user &>/dev/null || true
claude mcp remove jobspy &>/dev/null || true

# Register at user scope so it works in any project directory
claude mcp add -s user jobspy -- "$VENV/bin/python" "$SERVER_PY" &>/dev/null \
    || fail "Failed to register MCP server. Check that Claude Code CLI is installed."

ok "registered with Claude Code (user scope — works in any project)"

echo ""
echo -e "${GREEN}${BOLD}Setup complete!${NC}"
echo ""
echo "  Next: restart Claude Code so it picks up the new MCP server."
echo "  Then start jobbi — scrape_jobs_tool will be available."
echo ""
echo "  To uninstall:"
echo "    claude mcp remove jobspy -s user"
echo "    rm -rf $INSTALL_DIR"
echo ""
