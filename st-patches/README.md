自用的st的patch整合文件，包含以下patch和修改
+ alpha
+ dynamic cursor color
+ glyph wide support
+ ligatures
+ csi 22 23
+ scrollback
	+ st-scrollback-reflow-0.8.5.diff
+ 和一些我自己的修改：
	+ 修复鼠标汇报问题
	+ 修复scrollback-reflow对宽字符的截断和乱码问题
	+ 光标置于宽字符上，使st窗口失去焦点后，光标处将显示一个框住宽字符的正方形框
