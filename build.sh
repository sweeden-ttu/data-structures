#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
ALL_LANGUAGES=(rust go c cpp perl ruby csharp javascript typescript python java swift objective-c)
ARCHITECTURES=(arm64 x86_64)
TARGET_ARCH=""
HOST_ARCH=""
LANGUAGES=()
BUILD_TYPE="release"
VERBOSE=false

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    --all           Build all languages
    --lang LANG     Build specific language (can be used multiple times)
    --arch ARCH     Target architecture (arm64 or x86_64)
    --target ARCH   Cross-compile target architecture
    --host ARCH     Host architecture for cross-compilation
    --debug         Build in debug mode
    --release       Build in release mode (default)
    --releasedebuginfo  Build with debug info but optimized
    --verbose       Enable verbose output
    -h, --help      Show this help message

Supported languages: ${ALL_LANGUAGES[*]}
Supported architectures: ${ARCHITECTURES[*]}
EOF
    exit 0
}

log_info() {
    echo "[INFO] $*"
}

log_error() {
    echo "[ERROR] $*" >&2
}

detect_host_arch() {
    case "$(uname -m)" in
        aarch64|arm64)
            echo "arm64"
            ;;
        x86_64|amd64)
            echo "x86_64"
            ;;
        *)
            log_error "Unknown architecture: $(uname -m)"
            exit 1
            ;;
    esac
}

build_rust() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Rust for $target ($build_type)"
    
    local rust_target=""
    case "$target" in
        arm64)
            rust_target="aarch64-unknown-linux-gnu"
            ;;
        x86_64)
            rust_target="x86_64-unknown-linux-gnu"
            ;;
    esac
    
    local profile="release"
    [[ "$build_type" == "debug" ]] && profile="dev"
    
    cargo build --profile "$profile" --target "$rust_target"
}

build_go() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Go for $target ($build_type)"
    
    local go_arch=""
    case "$target" in
        arm64)
            go_arch="arm64"
            ;;
        x86_64)
            go_arch="amd64"
            ;;
    esac
    
    local ldflags=""
    [[ "$build_type" == "release" ]] && ldflags="-ldflags=\"-s -w\""
    
    GOARCH="$go_arch" go build $ldflags ./...
}

build_c() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building C for $target ($build_type)"
    
    local cc="${CC:-gcc}"
    local cflags="-Wall -Wextra"
    
    case "$target" in
        arm64)
            cflags="$cflags -target aarch64-linux-gnu"
            ;;
        x86_64)
            cflags="$cflags -target x86_64-linux-gnu"
            ;;
    esac
    
    [[ "$build_type" == "release" ]] && cflags="$cflags -O3"
    [[ "$build_type" == "releasedebuginfo" ]] && cflags="$cflags -O2 -g"
    [[ "$build_type" == "debug" ]] && cflags="$cflags -g -O0"
    
    make CC="$cc" CFLAGS="$cflags" ARCH="$target"
}

build_cpp() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building C++ for $target ($build_type)"
    
    local cxx="${CXX:-g++}"
    local cxxflags="-Wall -Wextra -std=c++17"
    
    case "$target" in
        arm64)
            cxxflags="$cxxflags -target aarch64-linux-gnu"
            ;;
        x86_64)
            cxxflags="$cxxflags -target x86_64-linux-gnu"
            ;;
    esac
    
    [[ "$build_type" == "release" ]] && cxxflags="$cxxflags -O3"
    [[ "$build_type" == "releasedebuginfo" ]] && cxxflags="$cxxflags -O2 -g"
    [[ "$build_type" == "debug" ]] && cxxflags="$cxxflags -g -O0"
    
    make CXX="$cxx" CXXFLAGS="$cxxflags" ARCH="$target"
}

build_python() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Python for $target ($build_type)"
    
    python -m build
    
    if command -v cython &>/dev/null; then
        log_info "Building Cython extensions"
        cythonize -i src/*.pyx 2>/dev/null || true
    fi
}

build_java() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Java for $target ($build_type)"
    
    mvn clean package -DskipTests
    
    if command -v native-image &>/dev/null; then
        log_info "Building native image for $target"
        case "$target" in
            arm64)
                native-image --target=arm64 -jar target/*.jar
                ;;
            x86_64)
                native-image --target=amd64 -jar target/*.jar
                ;;
        esac
    fi
}

build_javascript() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building JavaScript for $target ($build_type)"
    
    if [[ -f "package.json" ]]; then
        npm install
        npm run build
    fi
}

build_typescript() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building TypeScript for $target ($build_type)"
    
    if [[ -f "tsconfig.json" ]]; then
        tsc --project tsconfig.json
    fi
}

build_csharp() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building C# for $target ($build_type)"
    
    local config="Release"
    [[ "$build_type" == "debug" ]] && config="Debug"
    
    local runtime=""
    case "$target" in
        arm64)
            runtime="linux-arm64"
            ;;
        x86_64)
            runtime="linux-x64"
            ;;
    esac
    
    dotnet build -c "$config" -r "$runtime"
}

build_ruby() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Ruby for $target ($build_type)"
    
    if [[ -f "Gemfile" ]]; then
        bundle install
    fi
    
    if [[ -f "Rakefile" ]]; then
        rake
    fi
}

build_perl() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Perl for $target ($build_type)"
    
    if [[ -f "Makefile.PL" ]]; then
        perl Makefile.PL
        make
    elif [[ -f "Build.PL" ]]; then
        perl Build.PL
        ./Build
    fi
}

build_swift() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Swift for $target ($build_type)"
    
    local config="release"
    [[ "$build_type" == "debug" ]] && config="debug"
    
    swift build -c "$config"
}

build_objective_c() {
    local target="$1"
    local build_type="$2"
    
    log_info "Building Objective-C for $target ($build_type)"
    
    local cc="${CC:-clang}"
    local cflags="-Wall -Wextra -fobjc-arc"
    
    case "$target" in
        arm64)
            cflags="$cflags -target aarch64-linux-gnu"
            ;;
        x86_64)
            cflags="$cflags -target x86_64-linux-gnu"
            ;;
    esac
    
    [[ "$build_type" == "release" ]] && cflags="$cflags -O3"
    [[ "$build_type" == "releasedebuginfo" ]] && cflags="$cflags -O2 -g"
    [[ "$build_type" == "debug" ]] && cflags="$cflags -g -O0"
    
    make CC="$cc" CFLAGS="$cflags" ARCH="$target" OBJC=1
}

build_language() {
    local lang="$1"
    local arch="$2"
    local build_type="$3"
    
    case "$lang" in
        rust) build_rust "$arch" "$build_type" ;;
        go) build_go "$arch" "$build_type" ;;
        c) build_c "$arch" "$build_type" ;;
        cpp) build_cpp "$arch" "$build_type" ;;
        python) build_python "$arch" "$build_type" ;;
        java) build_java "$arch" "$build_type" ;;
        javascript) build_javascript "$arch" "$build_type" ;;
        typescript) build_typescript "$arch" "$build_type" ;;
        csharp) build_csharp "$arch" "$build_type" ;;
        ruby) build_ruby "$arch" "$build_type" ;;
        perl) build_perl "$arch" "$build_type" ;;
        swift) build_swift "$arch" "$build_type" ;;
        objective-c) build_objective_c "$arch" "$build_type" ;;
        *)
            log_error "Unknown language: $lang"
            return 1
            ;;
    esac
}

main() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --all)
                LANGUAGES=("${ALL_LANGUAGES[@]}")
                shift
                ;;
            --lang)
                LANGUAGES+=("$2")
                shift 2
                ;;
            --arch)
                TARGET_ARCH="$2"
                shift 2
                ;;
            --target)
                TARGET_ARCH="$2"
                shift 2
                ;;
            --host)
                HOST_ARCH="$2"
                shift 2
                ;;
            --debug)
                BUILD_TYPE="debug"
                shift
                ;;
            --release)
                BUILD_TYPE="release"
                shift
                ;;
            --releasedebuginfo)
                BUILD_TYPE="releasedebuginfo"
                shift
                ;;
            --release)
BUILD_TYPE="release"
RELEASE_DEBUG_INFO=false
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                usage
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                ;;
        esac
    done
    
    if [[ ${#LANGUAGES[@]} -eq 0 ]]; then
        log_error "No languages specified. Use --all or --lang <language>"
        usage
    fi
    
    : "${TARGET_ARCH:=$(detect_host_arch)}"
    : "${HOST_ARCH:=$(detect_host_arch)}"
    
    log_info "Build configuration:"
    log_info "  Languages: ${LANGUAGES[*]}"
    log_info "  Target arch: $TARGET_ARCH"
    log_info "  Host arch: $HOST_ARCH"
    log_info "  Build type: $BUILD_TYPE"
    
    for lang in "${LANGUAGES[@]}"; do
        log_info "Building $lang..."
        if build_language "$lang" "$TARGET_ARCH" "$BUILD_TYPE"; then
            log_info "Successfully built $lang"
        else
            log_error "Failed to build $lang"
        fi
    done
    
    log_info "Build complete!"
}

main "$@"
