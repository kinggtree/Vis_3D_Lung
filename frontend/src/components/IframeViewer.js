import React from 'react';
import { Paper, CircularProgress, Typography } from '@mui/material';

const IframeViewer = ({ iframeSrc, iframeKey, isIframeLoading, onLoad, onLoadStart }) => (
  <Paper elevation={3} className='model-container'>
    {isIframeLoading && (
      <div className="loading-container">
        <CircularProgress />
        <Typography>加载3D模型中...</Typography>
        <Typography>因网络问题，加载所用时间可能比预想的要长</Typography>
        <Typography>预计加载时长在 5~10 秒</Typography>
      </div>
    )}
    <iframe
      key={iframeKey}
      src={iframeSrc}
      title="Model Viewer"
      style={{ width: '100%', height: '100%', border: 'none', display: isIframeLoading ? 'none' : 'block' }}
      onLoad={onLoad}
      onLoadStart={onLoadStart}
    ></iframe>
  </Paper>
);

export default IframeViewer;
