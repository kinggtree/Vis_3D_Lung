import React from 'react';
import { Select, MenuItem, Button, Typography, CircularProgress, Box } from '@mui/material';

const SelectionControls = ({
  personListItems,
  layerListItems,
  lesionsLayerListItems,
  selectedPersonName,
  selectedLayerName,
  onPersonChange,
  onLayerChange,
  onReloadPerson,
  onReloadLayer,
  isLoading // 新增的加载状态
}) => (
  <Box className="option-container">
    {isLoading ? (
      <Box className="loading-container">
        <CircularProgress />
        <Typography>Loading...</Typography>
      </Box>
    ) : (
      <>
        <Typography variant="h6" gutterBottom className='tipText'>
          请选择病人
        </Typography>
        <Select value={selectedPersonName} onChange={onPersonChange} className='option' fullWidth>
          {personListItems.map(item => (
            <MenuItem key={item} value={item}>{item}</MenuItem>
          ))}
        </Select>
        <Button variant="contained" color="primary" onClick={onReloadPerson} className='button'>
          Reload Person
        </Button>
        {layerListItems.length > 0 && (
          <Box mt={2}>
            <Typography variant="h6" gutterBottom className='tipText'>
              请选择CT层
            </Typography>
            <Select value={selectedLayerName} onChange={onLayerChange} className='option' fullWidth>
              {layerListItems.map(item => (
                <MenuItem key={item} value={item}>{item}</MenuItem>
              ))}
            </Select>
            <Button variant="contained" color="primary" onClick={onReloadLayer} className='button'>
              Reload Layer
            </Button>
          </Box>
        )}
        {layerListItems.length > 0 && lesionsLayerListItems.length === 0 && (
          <Typography variant="body2" color="textSecondary" mt={2} className='tipText'>
            暂未发现病灶
          </Typography>
        )}
        {lesionsLayerListItems.length > 0 && (
          <Box mt={2}>
            <Typography variant="h6" gutterBottom className='tipText'>
              请选择存在病灶的CT层
            </Typography>
            <Select value={selectedLayerName} onChange={onLayerChange} className='option' fullWidth>
              {lesionsLayerListItems.map(item => (
                <MenuItem key={item} value={item}>{item}</MenuItem>
              ))}
            </Select>
            <Button variant="contained" color="primary" onClick={onReloadLayer} className='button'>
              Reload Lesions Layer
            </Button>
          </Box>
        )}
      </>
    )}
  </Box>
);

export default SelectionControls;
