import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Grid } from '@mui/material';
import SelectionControls from './SelectionControls';
import ImageDisplay from './ImageDisplay';
import IframeViewer from './IframeViewer';
import './styles.css'; // 引入 CSS 文件

function ModelViewer() {
  const [grayImage, setGrayImage] = useState('');
  const [maskedImage, setMaskedImage] = useState('');
  const [selectedPersonName, setSelectedPersonName] = useState('');
  const [selectedLayerName, setSelectedLayerName] = useState('');
  const [personListItems, setPersonListItems] = useState([]);
  const [layerListItems, setLayerListItems] = useState([]);
  const [lesionsLayerListItems, setLesionsLayerListItems] = useState([]);
  const [iframeKey, setIframeKey] = useState(0); // 用于重新加载 iframe 内容的 key
  const [iframeSrc, setIframeSrc] = useState('');
  const [isIframeLoading, setIsIframeLoading] = useState(true); // 用于跟踪 iframe 的加载状态
  const [isLoading, setIsLoading] = useState(false); // 新增的加载状态
  const [isImageLoading, setIsImageLoading] = useState(false); // 新增的图片加载状态
  const [isImageCleared, setIsImageCleared] = useState(false); // 新增的图片清除状态
  const [controlsKey, setControlsKey] = useState(0); // 用于强制刷新 SelectionControls

  useEffect(() => {
    // 获取第一张图片
    apiGetGrayImage();
    apiGetMaskedImage();

    apiGetPersonList();

    // 设置初始选项
    setSelectedPersonName('Select One');

    // 设置模型目录的默认值
    const hostname = window.location.hostname;
    const port = '5000'; // 后端端口号 5000
    const defaultModelPath = '../3d_model.html'; // 默认模型路径
    setIframeSrc(`http://${hostname}:${port}/api/htmlModel?modelPath=${defaultModelPath}`);

  }, []);

  // 获取所有表单（用于初始化或者刷新病人）
  const apiGetPersonList = () => {
    setIsLoading(true); // 开始加载
    // 获取人员列表项
    axios.get('/api/getPersonList')
      .then(response => {
        setPersonListItems(response.data);
        setIsLoading(false); // 加载完成
      })
      .catch(error => {
        console.error('Error fetching list items:', error);
        setIsLoading(false); // 加载失败，也设置为完成
      });
  };

  // 获取CT层列表
  const apiGetLayerList = (personFileName) => {
    setIsLoading(true); // 开始加载
    // 获取所有层列表
    axios.get('/api/getLayerList', {
      params: {
        personFileName: personFileName
      }
    })
      .then(response => {
        setLayerListItems(response.data);
        setIsLoading(false); // 加载完成
      })
      .catch(error => {
        console.error('Error fetching list items:', error);
        setIsLoading(false); // 加载失败，也设置为完成
      });

    // 获取病灶层列表
    axios.get('/api/getLesionsLayerList', {
      params: {
        personFileName: personFileName
      }
    })
      .then(response => {
        setLesionsLayerListItems(response.data);
        setIsLoading(false); // 加载完成
      })
      .catch(error => {
        console.error('Error fetching list items:', error);
        setIsLoading(false); // 加载失败，也设置为完成
      });
  };

  // 获取gray CT图，传入的index为层数编号
  const apiGetGrayImage = () => {
    setIsImageLoading(true); // 开始图片加载
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
        setIsImageLoading(false); // 图片加载完成
        setIsImageCleared(false); // 图片加载完成，清除状态设为 false
      })
      .catch(error => {
        console.error('Error fetching first image:', error);
        setIsImageLoading(false); // 图片加载失败，也设置为完成
      });
  };

  // 获取gray CT图，传入的index为层数编号
  const apiGetMaskedImage = () => {
    setIsImageLoading(true); // 开始图片加载
    axios.get('/api/getMaskedImage', {
      params: {
        layerName: selectedLayerName,
        personName: selectedPersonName
      },
      responseType: 'blob'
    })
      .then(response => {
        const imageUrl = URL.createObjectURL(response.data);
        setMaskedImage(imageUrl);
        setIsImageLoading(false); // 图片加载完成
        setIsImageCleared(false); // 图片加载完成，清除状态设为 false
      })
      .catch(error => {
        console.error('Error fetching first image:', error);
        setIsImageLoading(false); // 图片加载失败，也设置为完成
      });
  };

  // 重新获取选定病人所有信息
  const refreshNewPerson = () => {
    setSelectedLayerName(''); // 重置层数选择框的值
    setGrayImage(''); // 清空灰度图像
    setMaskedImage(''); // 清空掩码图像
    setIsImageCleared(true); // 设置图片清除状态为 true
    setControlsKey(prevKey => prevKey + 1); // 更新状态以触发 SelectionControls 重新渲染
    apiGetLayerList(selectedPersonName);
    axios.get('/api/refreshHtmlFile', {
      params: {
        personName: selectedPersonName
      }
    }).then(response => {
      const newModelPath = response.data.modelPath;
      const hostname = window.location.hostname;
      const port = '5000'; // 后端端口号 5000
      setIframeSrc(`http://${hostname}:${port}/api/htmlModel?modelPath=${newModelPath}`);
      setIframeKey(prevKey => prevKey + 1); // 更新状态以触发组件更新或重新渲染
      setIsIframeLoading(true); // 设置为加载中
    })
      .catch(error => {
        console.error('Error refreshing HTML file:', error);
      });
  };

  // 刷新病人图层
  const refreshNewLayer = () => {
    apiGetGrayImage();
    apiGetMaskedImage();
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
      <Grid item xs={12} sm={3} container direction="column" className='option-container'>
        <SelectionControls
          key={controlsKey} // 使用 key 来强制重新渲染
          personListItems={personListItems}
          layerListItems={layerListItems}
          lesionsLayerListItems={lesionsLayerListItems}
          selectedPersonName={selectedPersonName}
          selectedLayerName={selectedLayerName}
          onPersonChange={handlePersonSelectChange}
          onLayerChange={handleLayerSelectChange}
          onReloadPerson={refreshNewPerson}
          onReloadLayer={refreshNewLayer}
          isLoading={isLoading} // 传递加载状态
        />
      </Grid>

      <Grid item xs={12} sm={9}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <IframeViewer
              iframeSrc={iframeSrc}
              iframeKey={iframeKey}
              isIframeLoading={isIframeLoading}
              onLoad={() => setIsIframeLoading(false)}
              onLoadStart={() => setIsIframeLoading(true)}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <ImageDisplay
              grayImage={grayImage}
              maskedImage={maskedImage}
              isLoading={isImageLoading} // 传递图片加载状态
              isImageCleared={isImageCleared} // 传递图片清除状态
            />
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default ModelViewer;