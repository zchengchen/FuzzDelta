dir=$(pwd)
cd /home/zhicheng/FuzzDelta/experiments/aixcc_nginx
./run.sh -x build
docker cp /home/zhicheng/FuzzDelta/experiments/aixcc_nginx/out/pov_harness 0d74d91a1a2d:/work
docker cp /home/zhicheng/FuzzDelta/experiments/aixcc_nginx/out/smtp_harness 0d74d91a1a2d:/work
docker cp /home/zhicheng/FuzzDelta/experiments/aixcc_nginx/out/mail_request_harness 0d74d91a1a2d:/work
cd "$dir"