#!/bin/bash

cat << EOF
/*
 * Install ai_application
 */
EOF

ROOT_PATH=$(cd "$(dirname "$0")";pwd)
AIPARADISE_PATH="/usr/local/UBTTools/ai_paradise"
ICON_PATH="/usr/local/UBTTools/images/ai_paradise"

pushd $ROOT_PATH &> /dev/null

echo "1.Remove desktop&icon"

rm -rf ${AIPARADISE_PATH}
rm -rf ${ICON_PATH}

echo "2.Copy desktop&icon"

cp -ar desktop ${AIPARADISE_PATH}
chown oneai:oneai ${AIPARADISE_PATH}/*
cp -ar icons ${ICON_PATH}

echo "3.Remove AIParadise cache"

cd ..
rm -rf build dist

echo "4.unzip resource"
unzip face_recognize_demo/resources_rc.py.zip -d ./face_recognize_demo &> /dev/null

echo "5.Installing AIParadise"

python3 setup.py install &> /dev/null

popd &> /dev/null

echo "6.Done"
