#!/bin/bash

# 安装依赖（CentOS/Ubuntu/macOS）
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f /etc/redhat-release ]; then
        sudo yum install -y git curl vim cmake python3-devel nodejs npm  # CentOS
    else
        sudo apt update && sudo apt install -y git curl vim cmake python3-dev nodejs npm  # Ubuntu
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install git curl vim cmake python node  # macOS
fi

# 备份旧配置
[ -f ~/.vimrc ] && mv ~/.vimrc ~/.vimrc.bak
[ -d ~/.vim ] && mv ~/.vim ~/.vim.bak

# 安装插件管理器 (vim-plug)
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# 写入基础配置
cat > ~/.vimrc << 'EOF'
" 基础设置
set nocompatible
set number
set relativenumber
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set smartindent
set mouse=

" 插件列表
call plug#begin('~/.vim/plugged')

" 主题美化
Plug 'morhetz/gruvbox'
Plug 'vim-airline/vim-airline'

" 文件树
Plug 'preservim/nerdtree'

" 代码补全 (需要 Node.js)
Plug 'neoclide/coc.nvim', {'branch': 'release'}

" 模糊搜索
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" Git 集成
Plug 'tpope/vim-fugitive'
Plug 'airblade/vim-gitgutter'

" 自动格式化
Plug 'sbdchd/neoformat'

call plug#end()

" 主题配色
" colorscheme gruvbox
" set background=dark

" NERDTree 快捷键
map <C-n> :NERDTreeToggle<CR>

" coc.nvim 配置
let g:coc_global_extensions = ['coc-json', 'coc-pyright', 'coc-clangd', 'coc-tsserver']

" 模糊搜索快捷键
nnoremap <C-p> :Files<CR>
nnoremap <C-f> :Rg<CR>

" 在输入搜索模式时实时跳转到第一个匹配项
set incsearch
" 高亮所有匹配项
set hlsearch

" 保存时自动格式化
autocmd BufWritePre * Neoformat

" Alt+Left 跳到前一个单词开头（普通/可视模式）
execute "map \<Esc>b b"
execute "imap \<Esc>b \<Esc>bi"

" Alt+Right 跳到下一个单词开头（普通/可视模式）
execute "map \<Esc>f e"
execute "imap \<Esc>f \<Esc>ea"

" Enter 确认当前候选
inoremap <silent><expr> <CR>
      \ pumvisible() ? coc#_select_confirm()
      \ : "\<CR>"

" Tab 确认当前候选
inoremap <silent><expr> <Tab>
      \ pumvisible() ? coc#_select_confirm()
      \ : "\<CR>"
EOF

# 安装插件
vim +PlugInstall +qall

# 安装 coc.nvim 扩展
vim +'CocInstall -sync coc-json coc-pyright coc-clangd' +qall

echo "✅ Vim 配置完成！打开 Vim 输入 :PlugInstall 如果未自动安装插件。"
