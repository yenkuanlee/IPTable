sudo /etc/init.d/postgresql restart
sudo -u postgres psql -c "CREATE EXTENSION MULTICORN;"
sudo -u postgres psql -c "CREATE SERVER ipserver foreign data wrapper multicorn options (wrapper 'multicorn.ipfs_tablefdw.IPFSFdw');"
ipfs init
ipfs daemon &
python push_data.py
