## Mochimo miner monitoring

Monitor your miners from the [mochimo project](https://mochimo.org/). The web frontend can monitor hashrates, difficulty, GPU temperature, power usage and more.

![My image](https://raw.githubusercontent.com/0xFF0/MochimoMinerMonitoring/master/screenshot.png)

### Requirements

Tested on Ubuntu 16.04 and Nvidia GPU. 

	$ sudo apt-get install python3-pip
	$ pip3 install dash dash-core-components dash-html-components gpustat numpy pandas

### Usage

- [Setup](https://docs.google.com/document/d/1nxWO-O5fZ_xdJwqpZAkWtw1Zby6ENdQsoRQn8wY2EoU) and start mining
- Copy MochimoMonitoring.py in the ./bin directory
- Start the web server


		$ python3 MochimoMonitoring.py -d d
