#设置awk分隔符
BEGIN{FS = ",";}

{
#识别房价类型
if (FILENAME ~ /xinfang/){
    str_tail = "xinfang"
}
else if (FILENAME ~ /ershoufang/){
    str_tail = "ershoufang"
}
else if(FILENAME ~ /zufang/){
    str_tail = "zufang"
}

#按月份分类数据
print $0 >> (str_tail $1 ".csv")
}
