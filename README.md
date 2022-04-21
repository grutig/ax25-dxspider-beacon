# ax25-dxspider-beacon
ham radio ax25 packet radio beacon for dx-spider spots

My Rpi packet radio node currently has two active 'services'. 
The main one is a BBS (LinFBB) linked to -3 SSID.
The second one uses this software to run a beacon to broadcast DxCluster spots as I8ZSE-1. 
The beacon responds to commands sent over UI (connectionless) packets:
 - DXCLUSTER HELP command that broadcast a how-to-use message
 - DXCLUSTER <filter> allow you to set bandwidth and mode filters
Beacon remains active for 10 minutes after the last command.
During this time windows it will broadcast all the spots that satify the filters selected.
