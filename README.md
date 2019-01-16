
![Logo of Coinboot](https://raw.githubusercontent.com/frzb/coinboot/master/coinboot.png)

## Plugins for Coinboot

Coinboot is a framework for diskless computing.   
This repository contains plugins for Coinboot which expand Coinboot with further software and functionalities.  
It also contains `coinbootmaker` - a little helper to build your own Coinboot plugins.  
  
For more information how to boot your machines with Coinboot visit: https://coinboot.io

## Requirements 

* A running Coinboot setup

* Docker if you want to build plugins on your own

## Usage

### Pre-built Plugins

Put the pre-built plugins of your choice that your can download under [releases](https://github.com/frzb/coinboot-plugins/releases)
into the `plugins` directory of your Coinboot setup.

### Coinbootmaker - build the Plugins

To build Coinboot plugins on your own use `coinbootmaker`.

```
$ ./coinbootmaker <path to Coinboot Initramfs>
```

For example:

```
$ ./coinbootmaker /tmp/coinboot-initramfs-4.15.0-43-generic  
```

`coinbootmaker` takes a path to a Coinboot-Initramfs to create an environment for building the plugins  
by converting the given Initramfs into a Container image and run it.  
All plugin scripts located at `src` are than executed in that `coinbootmaker` container and the resulting  
plugin archives are written to the `build` directory.

## License

MIT

Please notice even while the scripts to create Coinboot plugins are licensed with the MIT license the software packaged by this scripts may be licensed by an other license with different terms and conditions.  
You have to agree to the license of the packaged software to use it.

## Author

Gunter Miegel 
gm@coinboot.io

## Contribution

Fork this repo. 
Make a pull request to this repo. 
