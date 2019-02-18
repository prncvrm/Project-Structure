# Project-Structure

## To use this
```sh
python3 project-s.py -s <absolute_path_to_project> -o <absolute_path_to_ouput_file> -id <comma_delimited_folders_to_exclude> -ie <comma_delimited_extensions_to_exclude_eg: .svg>  
```

The script automatically intakes the .gitignore file rules and parses it to ignore the pre-exisiting rules in git-ignore

Example :
```sh
python3 project-s.py -s "/home/user/project-new" -ie .svg,.png,.jpg,.js,.css -id static
```
