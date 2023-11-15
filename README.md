# drivehound
magic file signatures + python drive recovery magic 

## install and use

```

git clone https://github.com/mewmix/drivehound

cd drivehound

```

Edit recovery_tester.py with the drive path you want, in my example I have 

```
recover_data(drive=1)
```

Where drive=1 means physical disk 1 in Windows; the function is cross platform and will accept linux / mac paths or windows number & letter schemes. 
