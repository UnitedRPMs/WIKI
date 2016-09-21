#!/bin/sh
# /tmp/ - directory for temporary packages
# depends:
# dnf install createrepo repoview git python3-dnf-plugins-extras-repomanage rsync


# Create config ~/.ssh/config

# Host *.sourceforge.net
#    User YOUR_OS_USERNAME
#    IdentityFile ~/.ssh/id_rsa

while getopts "abcd" option;
do
 case $option in
a)
            echo "Mode F25"
            task=25
            ;;
b)
            echo "Mode F24"
            task=repository
            ;;
c)
            echo "Mode F26"
            task=26
            ;;
d)
            echo "Mode F27"
            task=27
            ;;
 :)
echo -e "option add_packages needs an argument"
exit
;;
  *)
echo -e "\e[31minvalid option...\e[0m"
exit
   ;;
    esac



echo -e "\e[31mCheck for updates...\e[0m"
#git pull

echo -e "\e[31mSign packages...\e[0m"
rpm --addsign /tmp/*.rpm
rpm --resign /tmp/*.rpm


wait ${!}

echo -e "\e[31mMove packages...\e[0m"
mv /tmp/*src.rpm srpm/
mv /tmp/*debuginfo*.rpm x86_64/debug/
mv /tmp/*.rpm x86_64/

wait ${!}

echo -e "\e[31mDelete old versions...\e[0m"
rm -v $(dnf repomanage --keep=2 --old x86_64/)
rm -v $(dnf repomanage --keep=2 --old x86_64/debug/)
rm -v $(dnf repomanage --keep=2 --old srpm/)

echo -e "\e[31mRebuild indexes...\e[0m"
cd x86_64/ && createrepo . -x "*debuginfo*" && repoview . -i "*debuginfo*" && cd ..
cd x86_64/debug/ && createrepo . && repoview . && cd ../..
cd srpm/ && createrepo . && repoview . && cd ..

wait ${!}

echo -e "\e[31mSign repodata...\e[0m"
gpg2 --yes --detach-sign --armor x86_64/repodata/repomd.xml
gpg2 --yes --detach-sign --armor x86_64/debug/repodata/repomd.xml
gpg2 --yes --detach-sign --armor srpm/repodata/repomd.xml

wait ${!}

echo -e "\e[31mSync with Sourceforge...\e[0m"

if [ ! -d 'x86_64' ] && [ ! -d 'srpm' ] ; then 
echo 'Paths x86_64 and srpm does not exist... searching'
if [ -d $task ]; then
cd $task
else
cd /home/URPMS/$task
fi
 fi

wait ${!}

rsync -av --delete -e ssh x86_64/repoview/ web.sourceforge.net:/home/project-web/unitedrpms/htdocs/x86_64/repoview/
rsync -av --delete -e ssh x86_64/debug/repoview/ web.sourceforge.net:/home/project-web/unitedrpms/htdocs/x86_64/debug/repoview/
rsync -av --delete -e ssh srpm/repoview/ web.sourceforge.net:/home/project-web/unitedrpms/htdocs/srpm/repoview/
rsync -av --exclude .git/ --delete -e ssh . frs.sourceforge.net:/home/frs/project/unitedrpms/$task/
done
