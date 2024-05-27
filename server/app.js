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
  const kmeansImgPath = path.join('../Processed_Data/kmeans_image', `kmeans_${personFileName}`);
  const grayItems = fs.readdirSync(grayImgPath);
  const kmeansItems = fs.readdirSync(kmeansImgPath);

  let shorterArray;
  let shorterArrayDir;
  
  // 比较两个数组的长度，找到较短的那一个
  if (grayItems.length <= kmeansItems.length) {
    shorterArray = grayItems;
    shorterArrayDir = grayImgPath;
  } else {
    shorterArray = kmeansItems;
    shorterArrayDir = kmeansImgPath;
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


app.get('/api/refreshHtmlFile', async (req, res) => {
  const personName = req.query.personName;
  if (!personName) {
    res.status(400).send('Missing personName parameter');
    return;
  }

  model_path = path.join('../Processed_Data/3D_model', `3d_model_${personName}.html`);

  // 返回更新后的 model_path
  res.send({ modelPath: model_path });
});


// 路由，用于提供HTML文件和图片资源的路径
app.get('/api/htmlModel', (req, res) => {
  // 设置响应头中的 Content-Type 字段为 text/html
  res.set('Content-Type', 'text/html');

  // 返回 HTML 文件
  res.sendFile(path.join(__dirname, `${model_path}`));
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
      console.log(`received ${layerName} at getGrayImage api`);
      imagePath = `Processed_Data/gray_image/gray_${personName}/${layerName}.jpg`;
    }

  // 返回图片文件
  res.sendFile(path.join(__dirname, '..', imagePath));
});


// 获取kmeans图片
app.get('/api/getKmeansImage', (req, res) => {
  const layerName = req.query.layerName;
  const personName = req.query.personName
  let imagePath = ''

  if (layerName == '')
  {
    // 发送初始化图片
    imagePath = `testimg${1}.png`;
  }
  else {
    imagePath = `Processed_Data/kmeans_image/kmeans_${personName}/${layerName}.jpg`;
    console.log(`received ${layerName} at getKmeansImage api`);
  }

  // 返回图片文件
  res.sendFile(path.join(__dirname, '..', imagePath));
});



// 启动服务器
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
