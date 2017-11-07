# 表格存储Comand Line Tool
>2017-11-05

# 命令
- help
- config
- ct(create_table)
- dt(delete_table)
- lt(list_table)
- gt(get_table)
- ut(update_table)
- use(use_table)
- me
- gr(get_row)
- pr(put_row)
- scan
- import
- export
- quit

# 非交互模式
```
./ts -c "";
./ts -e {endpoint} -i {accessid} -k {accesskey} -c "";
```

# 命令：config
> 用户配置

`参数详解：`
 
```
config 
    --endpoint "{endpoint}"
    --accessid "{access_id}"
    --accesskey "{access_key}"
    --instance "{instance_name}"
```

`样例：`

```
```

# 命令：create_table(ct)
> 创建表

`参数详解：`
 
```
ct 
    --name {table_name}       # 必须
    --cu {read_cu},{write_cu} # 可选，默认为0,0
    --ttl {time_to_live}      # 可选，默认为86400
    --version {max_verison}   # 可选，默认为-1
    
    --primary_key {primary_key} # 必须
```

`样例：`

```
```

# 命令：delete_table(dt)
> 删除指定的表

`参数详解：`
 
```
dt
    --name {table_name} 
    --force
```

`样例：`

```
```

# 命令：list_table(lt)
> 遍历表名

`参数详解：`
 
```
lt
```

`样例：`

```
```

# 命令：get_table(gt)
> 获取表的设置信息

`参数详解：`
 
```
gt
    --name {table_name}       # 在use模式下可选，非use模式下必选  
```

`样例：`

```
```

# 命令：update_table(ut)
> 修改表的设置信息

`参数详解：`
 
```
ut 
    --name {table_name}       # 必须
    --cu {read_cu},{write_cu} # 可选，默认为0,0
    --ttl {time_to_live}      # 可选，默认为86400
    --version {max_verison}   # 可选，默认为-1
```

`样例：`

```
```

# 命令：use_table(use)
> 关联一张表

`参数详解：`
 
```
use 
    --name {table_name}       # 必须
```

# 命令：me
> 显示关联的信息

`参数详解：`
 
```
me
```

# 命令：put_row(pr)
> 写入一行数据

`参数详解：`
 
```
pr
    --name  
    --primary_key
    --attribute 
    --expect_ignore|expect_exist|expect_not_exist
    --cond
    
    primary_key {type}:{column name},
        type: string,int
        
    attribute {type}:{column name}:{timestmp},
        type: string,int
        timestmp:
        
    cond {column name}:{condtion}:{value},
        condition: >,<,>=, <=,=,!=
        
```

`样例：`

```

```

# 命令：get_row(gr)
> 获取指定的一行数据

`参数详解：`
 
```
gr
    --name 
    --primary_key
    --cond
    --version
    --columns
    --vertical
    
    primary_key {column name},
    columns {column name},
    
    cond {column name}:{condtion}:{value},
        condition: >,<,>=, <=,=,!=
```

`样例：`

```
```

# 命令：scan
> 顺序遍历数据

`参数详解：`
 
```
scan 
    --name 
    --begin
    --end
    --cond
    --version
    --columns
    --limit
    --direction
    --vertical
    
    n(next)
    abort 
    
    begin {column name},
    end {column name},
    columns {column name},
    
    cond {column name}:{condtion}:{value},
        condition: >,<,>=, <=,=,!=
        
    direction
        FORARD, BACKWARD
```

`样例：`

```
```

# 命令：import
> 将本地数据导入

`参数详解：`
 
```
import 
    --name    
    --with_ts
    --file 
    --vertical
    
    导入支持两种模式，第一种是不带时间戳，第二种是带时间戳
```

`样例：`

```

#本地文件样式一
uid0 attr00:string:attr00_v,attr01:string:attr01_v,attr02:int:attr02_v  

#本地文件样式二
uid0 attr00:string:153009123:attr00_v,attr01:string:153009123:attr01_v,attr02:int:153009123:attr02_v 

```

# 命令：export
> 将数据下载到本地

`参数详解：`
 
```
export
    --name 
    --begin
    --end
    --cond
    --version
    --columns
    --limit
    --direction
    --vertical
```
