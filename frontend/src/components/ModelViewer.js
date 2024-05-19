import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Grid, Paper } from '@mui/material';
import './styles.css'; // 引入 CSS 文件

function ModelViewer() {
  const [firstImage, setFirstImage] = useState('');

  useEffect(() => {
    // 获取第一张图片
    axios.get('/api/getFirstImage', { responseType: 'blob' })
      .then(response => {
        const imageUrl = URL.createObjectURL(response.data);
        setFirstImage(imageUrl);
      })
      .catch(error => {
        console.error('Error fetching first image:', error);
      });
  }, []);

  return (
    <Grid container spacing={2} style={{ height: '100vh' }}>
      <Grid item xs={6}>
        <Paper elevation={3} style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {/* 使用 iframe 内嵌 HTML 文件 */}
          <iframe src="http://localhost:5000/api/getHtmlFile" title="Model Viewer" style={{ width: '100%', height: '100%', border: 'none' }}></iframe>
        </Paper>
      </Grid>
      <Grid item xs={6}>
        <Grid container spacing={2} className="image-container"> {/* 使用 className 添加样式 */}
          <Grid item xs={12}>
            <Paper elevation={3} className="image-container"> {/* 使用 className 添加样式 */}
              {/* 渲染图片 */}
              <img src={firstImage} alt="First Image" />
            </Paper>
          </Grid>
          {/* 这里可以继续添加其他 Grid item */}
        </Grid>
      </Grid>
    </Grid>
  );
}

export default ModelViewer;
