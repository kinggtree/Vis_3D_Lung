// server/server.js

const express = require('express');
const path = require('path');

const app = express();
const PORT = 5000; // 可以根据需要修改端口号

// 设置 CSP 头，允许内联脚本
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', "default-src 'self' 'unsafe-inline'; img-src *");
  next();
});


// 静态文件中间件，用于提供HTML文件和图片资源
app.use(express.static(path.join(__dirname, '../public')));

// 路由，用于提供HTML文件和图片资源的路径
app.get('/api/getHtmlFile', (req, res) => {
  // 设置响应头中的 Content-Type 字段为 text/html
  res.set('Content-Type', 'text/html');

  // 返回 HTML 文件
  res.sendFile(path.join(__dirname, '../3d_model.html'));
});

app.get('/api/getFirstImage', (req, res) => {
  // 返回第一张图片，你可以根据具体路径来读取图片并发送
  res.sendFile(path.join(__dirname, '../testimg.png'));
});

// app.get('/api/getSecondImage', (req, res) => {
//   // 返回第二张图片，你可以根据具体路径来读取图片并发送
//   res.sendFile(path.join(__dirname, '../public/images/second_image.jpg'));
// });

// 启动服务器
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
