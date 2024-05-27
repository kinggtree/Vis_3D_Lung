import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Grid, Paper, Select, MenuItem, Typography, Button } from '@mui/material';
import './styles.css'; // 引入 CSS 文件

function ModelViewer() {
  const [grayImage, setGrayImage] = useState('');
  const [kmeansImage, setKmeansImage] = useState('');
  const [selectedPersonName, setSelectedPersonName] = useState('');
  const [selectedLayerName, setSelectedLayerName] = useState('');
  const [personListItems, setPersonListItems] = useState([]);
  const [layerListItems, setLayerListItems] = useState([]);
  const [iframeKey, setIframeKey] = useState(0); // 用于重新加载 iframe 内容的 key




  useEffect(() => {
    // 获取第一张图片
    apiGetGrayImage();
    apiGetKmeansImage();

    
    apiGetPersonList();

    // 设置初始选项
    setSelectedPersonName('Select One');
  }, []);

  // 获取所有表单（用于初始化或者刷新病人）
  const apiGetPersonList = () => {
    // 获取人员列表项
    axios.get('/api/getPersonList')
    .then(response => {
      setPersonListItems(response.data);
    })
    .catch(error => {
      console.error('Error fetching list items:', error);
    });
  };

  // 获取CT层列表
  const apiGetLayerList = (personFileName) => {
    axios.get('/api/getLayerList', {
      params: {
        personFileName: personFileName
      }
    })
    .then(response => {
      setLayerListItems(response.data);
    })
    .catch(error => {
      console.error('Error fetching list items:', error);
    });
  };

  // 获取gray CT图，传入的index为层数编号
  const apiGetGrayImage = () => {
    axios.get('/api/getGrayImage', {
      params: {
        layerName: selectedLayerName,
        personName: selectedPersonName
      },
      responseType: 'blob'
    })
    .then(response => {
      const imageUrl = URL.createObjectURL(response.data);
      setGrayImage(imageUrl);
    })
    .catch(error => {
      console.error('Error fetching first image:', error);
    });
  };

  // 获取gray CT图，传入的index为层数编号
  const apiGetKmeansImage = () => {
    axios.get('/api/getKmeansImage', {
      params: {
        layerName: selectedLayerName,
        personName: selectedPersonName
      },
      responseType: 'blob'
    })
    .then(response => {
      const imageUrl = URL.createObjectURL(response.data);
      setKmeansImage(imageUrl);
    })
    .catch(error => {
      console.error('Error fetching first image:', error);
    });
  };
  
 
  // 重新获取选定病人所有信息
  const refreshNewPerson = () => {
    apiGetLayerList(selectedPersonName);
    axios.get('/api/refreshHtmlFile', {
      params: {
        personName: selectedPersonName
      }
    }).then(response => {
      setIframeKey(prevKey => prevKey + 1); // 更新状态以触发组件更新或重新渲染
    })
    .catch(error => {
      console.error('Error refreshing HTML file:', error);
    });    
  };

  // 刷新病人图层
  const refreshNewLayer = () => {
    apiGetGrayImage();
    apiGetKmeansImage();
  };

  // 处理病人框下拉选择框变化
  const handlePersonSelectChange = (event) => {
    setSelectedPersonName(event.target.value);
  };

  // 处理层数框下拉选择框变化
  const handleLayerSelectChange = (event) => {
    setSelectedLayerName(event.target.value);
  };



  return (
    <Grid container spacing={2}>
      <Grid item xs={2} container direction="column" className='option-container'>
        <Select value={selectedPersonName} onChange={handlePersonSelectChange} className='option'>
          {personListItems.map(item => (
            <MenuItem key={item} value={item}>{item}</MenuItem>
          ))}
        </Select>
        <Button variant="contained" color="primary" onClick={refreshNewPerson} className='button'>
          Reload Person
        </Button>
        <Select value={selectedLayerName} onChange={handleLayerSelectChange} className='option'>
          {layerListItems.map(item => (
            <MenuItem key={item} value={item}>{item}</MenuItem>
          ))}
        </Select>
        {/* 重新加载按钮 */}
        <Button variant="contained" color="primary" onClick={refreshNewLayer} className='button'>
          Reload Layer
        </Button>
      </Grid>

      {/* 使用 iframe 内嵌 HTML 文件 */}
      <Grid item xs={5}>
        <Paper elevation={3} className='model-container'>
          <iframe key={iframeKey} src="http://localhost:5000/api/htmlModel" title="Model Viewer" style={{ width: '100%', height: '100%', border: 'none' }}></iframe>
        </Paper>
      </Grid>

      {/* 渲染图片 */}
      <Grid item xs={5}>
        <Grid container spacing={2} className="image-container"> 
          <Grid item xs={12} direction="column" spacing={2}>
            <Paper elevation={3} className="image-container"> 
              <img src={grayImage} alt="Gray Image" />
            </Paper>
            <Paper elevation={3} className="image-container"> 
              <img src={kmeansImage} alt="Kmeans Image" />
            </Paper>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default ModelViewer;
