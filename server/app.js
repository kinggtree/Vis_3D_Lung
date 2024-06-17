// server/server.js

const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 5000;

let model_path = '../3d_model.html';


function getNiiFileNames(directory) {
  const niiFileNames = [];

  const items = fs.readdirSync(directory);

  items.forEach(item => {
      const itemPath = path.join(directory, item);
      const isFile = fs.statSync(itemPath).isFile();

      if (isFile) {
          if (path.extname(item) === '.nii') {
              // 获取文件名并省去后缀
              const fileName = path.basename(item, '.nii');
              niiFileNames.push(fileName);
          }
      } else {
          // 递归调用
          const subFolderFileNames = getNiiFileNames(itemPath);
          niiFileNames.push(...subFolderFileNames);
      }
  });

  return niiFileNames;
};


function getLayerNames(personFileName) {
  const grayImgPath = path.join('../Processed_Data/gray_image', `gray_${personFileName}`);
  const maskedImgPath = path.join('../Processed_Data/masked_img', `masked_${personFileName}`);
  const grayItems = fs.readdirSync(grayImgPath);
  const maskedItems = fs.readdirSync(maskedImgPath);

  let shorterArray;
  let shorterArrayDir;
  
  // 比较两个数组的长度，找到较短的那一个
  if (grayItems.length <= maskedItems.length) {
    shorterArray = grayItems;
    shorterArrayDir = grayImgPath;
  } else {
    shorterArray = maskedItems;
    shorterArrayDir = maskedImgPath;
  }

  const layerNames = [];

  shorterArray.forEach(item => {
    const itemPath = path.join(shorterArrayDir, item);
    const isFile = fs.statSync(itemPath).isFile();

    if (isFile && path.extname(item) === '.jpg') {
      // 获取文件名并省去后缀
      const fileName = path.basename(item, '.jpg');
      layerNames.push(fileName);
    }
  });

  // 返回较短的子数组
  return layerNames;
};


function getLesionsLayerNames(personFileName) {
  const lesionsJsonPath = path.join('../Processed_Data/lesions_json', `lesions_${personFileName}.json`);

  // 读取JSON文件
  const lesionsJson = JSON.parse(fs.readFileSync(lesionsJsonPath, 'utf8'));

  // 获取所有层
  const layers = lesionsJson.lesions_slices;

  // 将所有层的数字前面加上layer字母，并保存到一个数组中
  const layerNames = layers.map(layer => `layer${layer}`);

  // 目录中所有存在的层文件
  const existingLayerNames = getLayerNames(personFileName);

  // 过滤layerNames数组中的元素，使得最终的validLayerNames数组只包含那些在existingLayerNames数组中也存在的元素
  const validLayerNames = layerNames.filter(layerName => existingLayerNames.includes(layerName));

  // 返回处理后的层
  return validLayerNames;

}


// 设置 CSP 头，允许内联脚本
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', "default-src 'self' 'unsafe-inline'; img-src *");
  next();
});


// 静态文件中间件，用于提供HTML文件和图片资源
app.use(express.static(path.join(__dirname, '../public')));

// 获取人员名单
app.get('/api/getPersonList', (req, res) => {
  const personList = getNiiFileNames('../Data');
  res.json(personList);
});

// 获取所有层的名字
app.get('/api/getLayerList', (req, res) => {
  const fileName = req.query.personFileName;
  const layerNameList = getLayerNames(fileName);
  res.send(layerNameList.sort(function(a, b) {
    const numberA = parseInt(a.substring(5)); // 提取数字部分
    const numberB = parseInt(b.substring(5));
    return numberA - numberB; // 按数字排序
  }));
});


app.get('/api/getLesionsLayerList', (req, res) => {
  const fileName = req.query.personFileName;
  const lesionsLayerNameList = getLesionsLayerNames(fileName);
  res.send(lesionsLayerNameList.sort(function(a, b) {
    const numberA = parseInt(a.substring(5)); // 提取数字部分
    const numberB = parseInt(b.substring(5));
    return numberA - numberB; // 按数字排序
  }));
})


app.get('/api/refreshHtmlFile', (req, res) => {
  const personName = req.query.personName;
  if (!personName) {
    res.status(400).send('Missing personName parameter');
    return;
  }

  const modelPath = path.join('../Processed_Data/3D_model', `3d_model_${personName}.html`);

  // 返回更新后的 modelPath
  res.send({ modelPath });
});

app.get('/api/htmlModel', (req, res) => {
  const modelPath = req.query.modelPath;
  if (!modelPath) {
    res.status(400).send('Missing modelPath parameter');
    return;
  }

  // 设置响应头中的 Content-Type 字段为 text/html
  res.set('Content-Type', 'text/html');

  // 返回 HTML 文件
  res.sendFile(path.join(__dirname, modelPath));
});


// 获取gray图片
app.get('/api/getGrayImage', (req, res) => {
  const layerName = req.query.layerName;
  const personName = req.query.personName
  let imagePath = ''

  if (layerName == '')
    {
      // 发送初始化图片
      imagePath = `testimg${0}.png`;
    }
    else {
      imagePath = `Processed_Data/gray_image/gray_${personName}/${layerName}.jpg`;
    }

  // 返回图片文件
  res.sendFile(path.join(__dirname, '..', imagePath));
});


// 获取masked图片
app.get('/api/getMaskedImage', (req, res) => {
  const layerName = req.query.layerName;
  const personName = req.query.personName;
  let imagePath = ''

  if (layerName == '')
  {
    // 发送初始化图片
    imagePath = `testimg${1}.png`;
  }
  else {
    imagePath = `Processed_Data/masked_img/masked_${personName}/${layerName}.jpg`;
  }

  // 返回图片文件
  res.sendFile(path.join(__dirname, '..', imagePath));
});



// 启动服务器
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
