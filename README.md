# wikiscan wiki敏感信息扫描工具

### 功能设计说明

wikiscan是根据password、key等关键词在企业内网搭建的confluence wiki平台审计相关敏感文件和内容暴露的扫描工具，其设计思路如下：

- 根据关键词在wiki中进行全局搜索，如（password、pwd、Authorization、密码），将搜索结果的页面路径信息去重整理得到搜索匹配的所有url集合；
- 正则匹配url集合中是否为数据文件或代码形式的后缀，如（txt、csv、xml、xsl、log、py、php、java、jsp、go），这些文件中包含密码等字段的关键字且本身就不太适合作为public权限的文档存在于wiki中，因此直接将该url作为风险结果保存；
- 不满足敏感后缀的url继续进入下面的检测逻辑，通过request遍历请求每一个wiki页面，正则匹配敏感关键字符合正则模式的放入风险结果中保存；
- 日常的用户进行wiki文章编辑会出现很多带有密码关键字的语句，很多实际并不是包含真正的密码或认证的凭证，需要通过正则减少误报量。
- 部分用户对文章中的密码关键字的value值有时会使用如 xxxxx、中文：密码、123456等进行掩码显示，根据企业中具体场景，可在正则中可对这些内容进行排除；
- 尽管正则尽量降低了搜索关键字带来的误报，仍然可能会有一些各种各样的特殊情况，我们可以通过白名单来排除这些实际上确认后没这么敏感的url；
- 我们并没有使用confluence官方提供的搜索接口，因为想到通过cookie虽然每次可能需要重新获得cookie值，但其实感觉更灵活些。


此外，我们通过参数可以支持两种扫描模式，全局扫描和单页扫描。全局扫描可以通过参数指定扫描搜索结果的url条数，单页扫描可以通过参数输入具体的wiki url来扫描这个页面是否包含敏感内容。

### 程序使用帮助

wikiscan v1.0 命令行参数方式执行：

    USAGE:
        -l  wiki url，singlepage scan mode use.
        -c  Number of search results.
        -h  Show help information.
    
 -l：选填参数，单页扫描某个wiki url是否有敏感关键字；
 
 -c：必填参数，用于全局模式设置扫描搜索的结果条数；
 
 -h：帮助信息。

参数使用说明：-l 仅用于单页模式，-c 全局模式必填，单页模式无需填写

for example： python3 ./wikiscan -c 200 （扫描搜索出来的200个结果页） 
              python3 ./wikiscan -l http://your_wikidomain/pages/viewpage.action?pageId=1234567 (单页模式）

程序更新列表

    v1.0 初始版本

