import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Grid, Paper, Select, MenuItem, Typography, Button } from '@mui/material';
import './styles.css'; // 引入 CSS 文件

function ModelViewer() {
  const [firstImage, setFirstImage] = useState('');
  const [selectedPersonOption, setSelectedPersonOption] = useState('');
  const [selectedLayerOption, setSelectedLayerOption] = useState('');
  const [personListItems, setPersonListItems] = useState([]);
  const [layerListItems, setLayerListItems] = useState([]);
  const [iframeKey, setIframeKey] = useState(0); // 用于重新加载 iframe 内容的 key




  useEffect(() => {
    // 获取第一张图片
    apiGetFirstImage(0);
    
    apiGetAllList();

    // 设置初始选项
    setSelectedPersonOption('Select One');
  }, []);

  // 获取所有表单（用于初始化或者刷新病人）
  const apiGetAllList = () => {
    // 获取人员列表项
    axios.get('/api/getAllListItems')
    .then(response => {
      setPersonListItems(response.data[0]);
      setLayerListItems(response.data[1]);
    })
    .catch(error => {
      console.error('Error fetching list items:', error);
    });
  };

  // 获取第一张CT图，传入的index为层数编号
  const apiGetFirstImage = (layerIndex) => {
    axios.get('/api/getFirstImage', {
      params: {
        layerIndex: layerIndex
      },
      responseType: 'blob'
    })
    .then(response => {
      const imageUrl = URL.createObjectURL(response.data);
      setFirstImage(imageUrl);
    })
    .catch(error => {
      console.error('Error fetching first image:', error);
    });
  };
  
 
  // 重新获取选定病人所有信息
  const refreshNewPerson = () => {
    apiGetAllList();
    apiGetFirstImage(0);
    setIframeKey(prevKey => prevKey + 1);
  };

  const refreshNewLayer = () => {
    let index = selectedLayerOption.charAt(selectedLayerOption.length - 1);
    apiGetFirstImage(index);
  };

  // 处理病人框下拉选择框变化
  const handlePersonSelectChange = (event) => {
    setSelectedPersonOption(event.target.value);
  };

  // 处理层数框下拉选择框变化
  const handleLayerSelectChange = (event) => {
    setSelectedLayerOption(event.target.value);
  };



  return (
    <Grid container spacing={2} style={{ height: '100vh' }}>
      <Grid item xs={2}>
        <Select value={selectedPersonOption} onChange={handlePersonSelectChange}>
          {personListItems.map(item => (
            <MenuItem key={item.id} value={item.value}>{item.label}</MenuItem>
          ))}
        </Select>
        <Button variant="contained" color="primary" onClick={refreshNewPerson}>
          Reload Person
        </Button>
        <Select value={selectedLayerOption} onChange={handleLayerSelectChange}>
          {layerListItems.map(item => (
            <MenuItem key={item.id} value={item.value}>{item.label}</MenuItem>
          ))}
        </Select>
        {/* 重新加载按钮 */}
        <Button variant="contained" color="primary" onClick={refreshNewLayer}>
          Reload Layer
        </Button>
      </Grid>
      <Grid item xs={5}>
        <Paper elevation={3} style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {/* 使用 iframe 内嵌 HTML 文件 */}
          <iframe key={iframeKey} src="http://localhost:5000/api/getHtmlFile" title="Model Viewer" style={{ width: '100%', height: '100%', border: 'none' }}></iframe>
        </Paper>
      </Grid>
      <Grid item xs={5}>
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
