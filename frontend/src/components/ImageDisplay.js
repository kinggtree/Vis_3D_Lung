import React from 'react';
import { Grid, Paper, Typography, CircularProgress, Box } from '@mui/material';

const ImageDisplay = ({ grayImage, maskedImage, isLoading, isImageCleared }) => (
  <Grid container spacing={2} className="image-container">
    <Grid item xs={12} direction="column" spacing={2}>
      {isLoading ? (
        <div className="loading-container">
          <CircularProgress />
          <Typography>Loading images...</Typography>
        </div>
      ) : isImageCleared ? (
        <Typography variant="h6" color="textSecondary">
          图片已清除，请选择新的病人和层数。
        </Typography>
      ) : (
        <>
          <Paper elevation={3} className="image-container">
            <img src={grayImage} alt="Gray Image" />
          </Paper>
          <Paper elevation={3} className="image-container">
            <img src={maskedImage} alt="Masked Image" />
          </Paper>
        </>
      )}
    </Grid>
  </Grid>
);

export default ImageDisplay;
