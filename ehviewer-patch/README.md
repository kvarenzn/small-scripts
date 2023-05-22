## 说明
自用的NekoInverter版EhViewer的修改部分，相比于原版，进行了如下修改
+ 修复了ehentai改版后无法跳页的问题
    + 这部分代码参考自[Ehviewer-Overhauled](https://github.com/Ehviewer-Overhauled/Ehviewer)，在此致谢
+ 修复了ehentai再次改版后缩略图无法加载的问题

## 使用
```
git clone --recursive https://gitlab.com/NekoInverter/EhViewer.git
cd EhViewer
patch < EhViewer.patch
```
之后使用AndroidStudio编译

由于缺失签名文件所以只能编译debug版，不过又不是不能用

原来直接`./gradlew build`也是可以的，不过最近不行了
