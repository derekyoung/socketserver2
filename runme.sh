python cli.py --loglevel=info --logfile=log/socket listen \
       --host=0.0.0.0 \
       --port=15001 \
       --datadir=data \
       --post-processing=bin/decodeit.py \
       --max-connections=100

