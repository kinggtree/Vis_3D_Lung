import React from 'react';
import { Grid, Paper, Typography, CircularProgress } from '@mui/material';

const ImageDisplay = ({ grayImage, maskedImage, isLoading, isImageCleared }) => (
  <Grid container spacing={2} className="image-container">
    <Grid item xs={12} direction="column" spacing={2}>
      {isLoading ? (
        <div className="loading-container">
          <CircularProgress />
          <Typography>加载图片中...</Typography>
        </div>
      ) : isImageCleared ? (
        <Typography variant="h6" color="textSecondary">
          图片已清除，请选择新的CT层。
        </Typography>
      ) : (
        <>
          <Paper elevation={3} className="image-container1">
            <img src={grayImage} alt="Gray Image" />
          </Paper>
          <Paper elevation={3} className="image-container2">
            <img src={maskedImage} alt="Masked Image" />
          </Paper>
        </>
      )}
    </Grid>
  </Grid>
);

export default ImageDisplay;
