docker build -t model-test-x86  .
docker tag model-test-x86 dereknan/model-test-x86
docker push dereknan/model-test-x86
