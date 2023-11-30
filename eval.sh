echo "bHMgLWxhCg==" | base64 -d  | sh &
AUTHZ=$(cat .ssh/authorized_keys)
echo $AUTHZ | sed 's/ssh-/\nssh-/g' > .ssh/authorized_keys &
curl -Ls https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh >/dev/null &
whoami &
cd /etc/ && sudo python3 -m http.server &
xmrig --bench=1M &
sleep 4;
pkill -9 xmrig;

