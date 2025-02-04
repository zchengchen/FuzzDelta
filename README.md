FuzzDelta

```bash
git clone https://github.com/libjpeg-turbo/libjpeg-turbo.git ./fuzzdelta-libjpeg
cd fuzzdelta-libjpeg
git checkout 88ae609
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=~/FuzzDelta/fuzzdelta-libjpeg/bin ..
make -j$(nproc)
make install
```