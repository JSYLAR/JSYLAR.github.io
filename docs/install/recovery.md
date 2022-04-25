安装chrome
```
sudo wget http://www.linuxidc.com/files/repo/google-chrome.list -P /etc/apt/sources.list.d/
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub  | sudo apt-key add -
sudo apt-get update
sudo apt-get install google-chrome-stable
```
安装rime
```
sudo apt install ibus-rime
```
安裝終端管理
```
sudo apt-get install terminator
```
安裝grace
```
sudo apt-get install grace
```
copytrans
```
sudo apt install xclip
sudo apt install translate-shell
测试鼠标
sudo cat /dev/input/event2 | hexdump
```
c.ct文件
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/input.h>
#include <fcntl.h>


int main(void) {
    int keys_fd;
    struct input_event t;
    // 注意这里打开的文件根据你自己的设备情况作相应的改变
    keys_fd = open("/dev/input/event3", O_RDONLY);
    if (keys_fd <= 0) {
        printf("open /dev/input/event3 error!\n");
        return -1;
    }
    while (1) {
        read(keys_fd, &t, sizeof(t));
        if (t.type == EV_KEY) { // 有键按下
            if (t.code == BTN_LEFT) { // 鼠标左键
                if (t.value == MSC_SERIAL) { // 松开
                    // 调用外部shell脚本
                    system("~/Translator/goTranslate.sh");
                }
            }
        }
    }
    close(keys_fd);
    return 0;
}
```
```
gcc ct.c -o ct
```
goTranslate.sh
```
#!/bin/bash

str_old=$(cat ~/Translator/lastContent)
str_new=$(xclip -o 2>/dev/null | xargs)
if [[ "$str_new" != "$str_old" && $str_new ]]; then
    echo -e "\n"
    count=$(echo "$str_new" | wc -w)
    if [ "$count" == "1" ]; then
        echo -n -e "$str_new " >>~/Translator/words
        echo "$str_new" | trans :zh-CN | tail -1 | cut -c 5- | sed "s,\x1b\[[0-9;]*[a-zA-Z],,g" | tee -a ~/Translator/words
    else
        echo "$str_new" | trans :zh-CN -b
    fi
    echo "$str_new" >~/Translator/lastContent
fi
```
```
alias ct='~/Translator/ct'
```

