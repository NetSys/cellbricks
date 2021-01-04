# Benchmarks (μTCell)


### Setup (EC2 VM)
* MPTCP Enabled (v0.94) AMI: `ami-06b93cd6edfe1ee9f` (perfd-cellular-stage-5, us-west-1)
* MPTCP Disabled AMI: `ami-0849b21b423a6baaa` (perfd-cellular-mptcp_disabled, us-west-1)

These AMI include mobile applications (more to be added in the long run) with datasets and scripts to start benchmarking, described in what follows. 
* Network benchmarks: iperf/iperf3, wrk 
* Video streaming (RTMP, HLS):  nginx-rtmp-module, ffmpeg
* Multimedia communication (e.g. SIP, RTP): [PJSIP](https://github.com/pjsip/pjproject)
* Web: [mitmproxy](https://github.com/mitmproxy/mitmproxy)

Pre-built docker image silveryfu/celleval:app (to be used with the tunnel setup, see /ho_proxy) includes the application benchmarks (same as the AMIs) and can be used at both the client- and server-side.

>TBD run application benchmarks on VM

### Setup (Docker container)

Applications are located in the /home directory of the container image:
```
root@bee1ebeb501a:/# ls /home
iperf  sip  video  web
```

iperf (iperf3):
* Refer to `man iperf3`
* Note: use `iperf3 -R` from the UE side to let the server to send traffic; current MPTCP implementation has a "server_side" flag that prohibits non TCP initiator to start subflow.

web page loading:
* `cd /home/web`
* Server-side: `make web`
* Client-side: `make client` (run `make test` first to check if the server is running)
* The client side will generate a web request every second and reports the completion time

video streaming:
* Mount video clips from the host/VM to the container, i.e., ` -v /mnt/clips:/mnt/clips` 
* Start nginx (run `nginx`);
* Run `FILE=../clips/[videofile] make stream` under `/mnt/hls/`
* 480p clip: `/mnt/clips/bun480p.mp4` (33s)
* 1080p clip: `/mnt/clips/greenland.mp4` (159s)
* Note: for all benchmarks remember to configure the EC2 security groups to allow traffic of the particular protocols and ports.

SIP (PJSIP):

* Register a SIP account (e.g., onsip.com)
* Run pjproject/pjsip-apps/bin/[binary] with --null-audio option [TBD: Makefile]
* [WIP]

Complete docker run command:
```
docker run -v /mnt/clips:/mnt/clips --name=uec -itd silveryfu/celleval:app /bin/bash
```



