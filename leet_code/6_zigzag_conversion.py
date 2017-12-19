"""
The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this:
(you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"
Write the code that will take a string and make this conversion given a number of rows:

string convert(string text, int nRows);
convert("PAYPALISHIRING", 3) should return "PAHNAPLSIIGYIR".

"""

__author__ = "Aollio Hou"
__email__ = "aollio@outlook.com"



class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        rows = []
        # initialize all row
        for x in range(numRows):
            rows.append([])

        series = self.strangely_series(numRows, len(s))

        for index, char in enumerate(s):
            rows[series[index]].append(char)
        result = ''
        for row in rows:
            result += ''.join(row)
        return result

    def strangely_series(self, n, length):
        """
        generate series like 0 1 2 3 2 1 0 1 2 3 ... (n = 4)
        """
        if n == 1:
            return [0] * length
        series = [0]
        up = True
        for index in range(1, length):
            pre = series[-1]
            if up:
                if pre == n - 1:
                    series.append(pre - 1)
                    up = False
                else:
                    series.append(pre + 1)
            else:
                if pre == 0:
                    series.append(pre + 1)
                    up = True
                else:
                    series.append(pre - 1)
        return series


print(Solution().strangely_series(2, 3))
s = 'PAYPALISHIRING'
numRows = 3
print(Solution().convert('ABC', 1))
