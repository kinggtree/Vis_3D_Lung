import React from 'react';
import { Paper, CircularProgress, Typography } from '@mui/material';

const IframeViewer = ({ iframeSrc, iframeKey, isIframeLoading, onLoad, onLoadStart }) => (
  <Paper elevation={3} className='model-container'>
    {isIframeLoading && (
      <div className="loading-container">
        <CircularProgress />
        <Typography>Loading...</Typography>
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
