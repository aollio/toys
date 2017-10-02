

Write a function to find the longest common prefix string amongst an array of strings.



**思路：**

找出一组数的最长前缀。那么这个前缀的长度肯定不大于这组数中最短字符串的长度。

遍历每个字符串。每个字符串的首字母作为根节点，随后字符作为子节点，递归。
这样会形成一课树。
在树的顶部，每个父节点只有一个子节点，那么则是前缀的一部分。
如果某个父节点含有大于一个子节点，则说明肯定有字符串在这个位置上的字符串是不同。
找出最大前缀，并返回

![adas](http://image.aollio.com/find-max-length-prefix-string.png)