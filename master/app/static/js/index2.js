  dc0 = new DICOMZero();
  const element = document.getElementById('dicomImage');
  const dropZone = document.getElementById('dropZone');
  url=window.location.href;
  var id_image = url.substring(url.lastIndexOf('/') + 1);
  cornerstone.enable(element);
  

  function resetDICOMzero() {
    dc0.reset();
  }

  

  function populatePixelArrayForFrame (pixels, frame, pixelData) {
    const bitArray = DCMJS.data.packBitArray(pixelData);
    const numBitArrayPixels = bitArray.length;
    let index = frame * numBitArrayPixels;
    for (let i=0; i < numBitArrayPixels; i++) {
      pixels[index++] = bitArray[i];
    }
  }

  function populateSegmentationObjectPixelData(dataset) {
    const pixels = new Uint8Array(dataset.PixelData);
    const configuration = cornerstoneTools.brush.getConfiguration();
    const brushLayerId = configuration.brushLayerId;

    // TODO: clean this up, it's super hacky
    const toolState = cornerstoneTools.globalImageIdSpecificToolStateManager.saveToolState();

    const numFrames = Number(dataset.NumberOfFrames);
    //const baseImageId = 'dicomweb:' + 'https://s3.amazonaws.com/IsomicsPublic/SampleData/MRHead/MRHead-8-slices.dcm';
    const baseImageId='dicomweb:'+'http://127.0.0.1/uploads/MRHead-8-slices.dcm';
    const getBrushPixelData = (imageId) => {
      // TODO: Might be a better way to do this...
      let pixelData;
      if (toolState[imageId] && toolState[imageId].brush) {
        pixelData = toolState[imageId].brush.data[0].pixelData;
      } else {
        pixelData = new Uint8ClampedArray(dataset.Rows * dataset.Columns);
      }
      return pixelData;
    };

    for (let frame = 0; frame < numFrames; frame++) {
      const imageId = baseImageId + '?frame=' + frame;
      const pixelData = getBrushPixelData(imageId);

      populatePixelArrayForFrame(pixels, frame, pixelData);
    }
  }

  $('#sampleData').click(function(event) {
    drawSampleDatasets();
  });

  function getImageIds(multiframe, baseImageId) {
    const imageIds = [];
    const numFrames = Number(multiframe.NumberOfFrames);
    for (let i=0; i < numFrames; i++) {
      let segNum;
      if (multiframe.PerFrameFunctionalGroupsSequence[i].SegmentIdentificationSequence) {
        segNum = multiframe.PerFrameFunctionalGroupsSequence[i].SegmentIdentificationSequence.ReferencedSegmentNumber;
      }
      const imageId = baseImageId + '?frame=' + i;
      imageIds.push(imageId);
    }
    return imageIds;
  }
  function activateCornerstoneStack() {
    // activates the dc0 singleton stack that has been set up either with
    // demo data or with user data

      cornerstone.loadAndCacheImage(dc0.cornerstoneStack.imageIds[0]).then(function(image) {
      // console.log(image);
      cornerstone.addLayer(element, image);
      cornerstone.updateImage(element);

      cornerstoneTools.addStackStateManager(element, ['stack']);
      cornerstoneTools.addToolState(element, 'stack', dc0.cornerstoneStack);



      cornerstoneTools.mouseInput.enable(element);
      cornerstoneTools.mouseWheelInput.enable(element);
      cornerstoneTools.keyboardInput.enable(element);
      cornerstoneTools.brush.activate(element, 1);
      setBrushRadius();
      cornerstoneTools.pan.activate(element, 2);
      cornerstoneTools.zoom.activate(element, 4);
      cornerstoneTools.stackScrollWheel.activate(element);
      cornerstoneTools.stackScrollKeyboard.activate(element);
    });
  }
  
  
  function drawData() {
    cornerstone.disable(element);
    cornerstone.enable(element);
    cornerstoneTools.clearToolState(element, 'stack');

    //var baseImageId = 'dicomweb:' + 'https://s3.amazonaws.com/IsomicsPublic/SampleData/MRHead/MRHead-8-slices.dcm'
    const baseImageId='dicomweb:'+'http://127.0.0.1/uploads/MRHead-8-slices.dcm';
    
    var dataPromise = loadMultiFrameAndPopulateMetadata(baseImageId);
    Promise.all([dataPromise,]).then(values => {
      dc0.multiframe = values[0];
      dc0.seg = new DCMJS.derivations.Segmentation([dc0.multiframe]);

      var cielab = DCMJS.data.Colors.rgb2DICOMLAB([1, 0, 0]);
      dc0.seg.dataset.SegmentSequence[0].RecommendedDisplayCIELabValue = cielab;
      var imageIds = getImageIds(dc0.multiframe, baseImageId);

      dc0.cornerstoneStack = {
        imageIds: imageIds,
        currentImageIdIndex: 0,
        options: {
          name: 'Referenced Image'
        }
      };
      activateCornerstoneStack();

    });
  }
  
   
  
   function drawSampleDatasets2(filename) {
    cornerstone.disable(element);
    cornerstone.enable(element);
    cornerstoneTools.clearToolState(element, 'stack');

    //var baseImageId = 'dicomweb:' + 'https://s3.amazonaws.com/IsomicsPublic/SampleData/MRHead/MRHead-8-slices.dcm'
    const baseImageId='dicomweb:'+'http://127.0.0.1/uploads/'+filename;
    
    var dataPromise = loadMultiFrameAndPopulateMetadata(baseImageId);

    Promise.all([dataPromise,]).then(values => {
      dc0.multiframe = values[0];
      dc0.seg = new DCMJS.derivations.Segmentation([dc0.multiframe]);

      var cielab = DCMJS.data.Colors.rgb2DICOMLAB([1, 0, 0]);
      dc0.seg.dataset.SegmentSequence[0].RecommendedDisplayCIELabValue = cielab;
      var imageIds = getImageIds(dc0.multiframe, baseImageId);
      dc0.cornerstoneStack={
        imageIds:imageIds,
        currentImageIdIndex:0,
        options:{
          name:"Referenced Image"
        }
      };
      activateCornerstoneStack();
      /*dc0.cornerstoneStack = {
        imageIds: imageIds,
        currentImageIdIndex: 0,
        options: {
          name: 'Referenced Image'
        }
      };
      activateCornerstoneStack();
      */
    });
  }

  function drawSampleDatasets() {
    cornerstone.disable(element);
    cornerstone.enable(element);
    cornerstoneTools.clearToolState(element, 'stack');

    //var baseImageId = 'dicomweb:' + 'https://s3.amazonaws.com/IsomicsPublic/SampleData/MRHead/MRHead-8-slices.dcm'
    const baseImageId='dicomweb:'+'http://127.0.0.1/uploads/MRHead-8-slices.dcm';
    
    var dataPromise = loadMultiFrameAndPopulateMetadata(baseImageId);
    Promise.all([dataPromise,]).then(values => {
      dc0.multiframe = values[0];
      dc0.seg = new DCMJS.derivations.Segmentation([dc0.multiframe]);

      var cielab = DCMJS.data.Colors.rgb2DICOMLAB([1, 0, 0]);
      dc0.seg.dataset.SegmentSequence[0].RecommendedDisplayCIELabValue = cielab;
      var imageIds = getImageIds(dc0.multiframe, baseImageId);

      dc0.cornerstoneStack = {
        imageIds: imageIds,
        currentImageIdIndex: 0,
        options: {
          name: 'Referenced Image'
        }
      };
      activateCornerstoneStack();

    });
  }

  var metaData = {};



  function loadAndViewImage2(imageId) {
      var element = document.getElementById('dicomImage');

      try {
          var start = new Date().getTime();
          cornerstone.loadAndCacheImage(imageId).then(function(image) {
              console.log(image);
              var viewport = cornerstone.getDefaultViewportForImage(element, image);
              cornerstone.displayImage(element, image, viewport);
              if(loaded === false) {
                  cornerstoneTools.mouseInput.enable(element);
                  cornerstoneTools.mouseWheelInput.enable(element);
                  cornerstoneTools.wwwc.activate(element, 1); // ww/wc is the default tool for left mouse button
                  cornerstoneTools.pan.activate(element, 2); // pan is the default tool for middle mouse button
                  cornerstoneTools.zoom.activate(element, 4); // zoom is the default tool for right mouse button
                  cornerstoneTools.zoomWheel.activate(element); // zoom is the default tool for middle mouse wheel
                  loaded = true;
              }

          }, function(err) {
              alert(err);
          });
      }
      catch(err) {
          alert(err);
      }
  }

  function addMetaData(type, imageId, data) {
    metaData[imageId] = metaData[imageId] || {};
    metaData[imageId][type] = data;
  }

  function loadFrameAndPopulateMetadata(baseImageId){
    const imageId=baseImageId;
    const element=document.getElementById('dicomImage');
    cornerstone.enable(element);
    cornerstone.loadImage(imageId).then(function(image){
      cornerstone.displayImage(element,image);
    });
  }

  function loadMultiFrameAndPopulateMetadata(baseImageId) {
    var promise = new Promise(function (resolve, reject) {
      cornerstone.loadAndCacheImage(baseImageId).then(function(image) {
        var arrayBuffer = image.data.byteArray.buffer;
        dicomData = DCMJS.data.DicomMessage.readFile(arrayBuffer);
        let dataset = DCMJS.data.DicomMetaDictionary.naturalizeDataset(dicomData.dict);
        dataset._meta = DCMJS.data.DicomMetaDictionary.namifyDataset(dicomData.meta);

        var multiframe = DCMJS.normalizers.Normalizer.normalizeToDataset([dataset]);
        const numFrames=Number(multiframe.NumberOfFrames);
        console.log(numFrames);
        //console.log(multiframe);

        /*const numFrames = Number(multiframe.NumberOfFrames);
        console.log(numFrames);
        for (let i=0; i < numFrames; i++) {
          const imageId = baseImageId + '?frame=' + i;

          var functionalGroup = multiframe.PerFrameFunctionalGroupsSequence[i];
          var imagePositionArray = functionalGroup.PlanePositionSequence.ImagePositionPatient;

          addMetaData('imagePlane', imageId, {
            imagePositionPatient: {
              x: imagePositionArray[0],
              y: imagePositionArray[1],
              z: imagePositionArray[2],
            }
          });
        }*/

        resolve(multiframe);
      });
    });

    return promise;
  }

  function drawDatasets() {
    cornerstone.disable(element);
    cornerstone.enable(element);
    cornerstoneTools.clearToolState(element, 'stack');

    var files = dc0.dataTransfer.files;
    var imageIds = [];
    files.forEach(function(file) {
      var imageId = cornerstoneWADOImageLoader.wadouri.fileManager.add(file);
      imageIds.push(imageId);
    });

    dc0.cornerstoneStack = {
      imageIds: imageIds,
      currentImageIdIndex: 0
    };
    activateCornerstoneStack();
    status(`Ready`);
  }

  function downloadDatasets() {
    populateSegmentationObjectPixelData(dc0.seg.dataset);
    $('#segmentationDump').text(JSON.stringify(dc0.seg.dataset, null,4));
    let multiBlob = DCMJS.data.datasetToBlob(dc0.multiframe);
    let segBlob = DCMJS.data.datasetToBlob(dc0.seg.dataset);
    // let zip = new JSZip();
    // zip.file("multiframe.dcm", multiBlob);
    // zip.file("segmentation.dcm", segBlob);
    // zip.generateAsync({type: "blob"})
    //   .then(function(contents) {
    //     saveAs(contents, "derivedDICOM.zip", true);
    //     resetDICOMzero();
    //     status(`Finished, waiting for more DICOM files (drop them below).`);
    //   });

    
  }

  // utility: todo: keep a log for optional download
  function status(s) {
    console.log('status: ', s);
    $('#status').text(s);
  }


  resetDICOMzero();

  window.addEventListener('resize', function() {
    dropZone.width = window.innerWidth;
    dropZone.height = window.innerHeight;
    cornerstone.resize(element, true);
  });

  window.dispatchEvent(new Event('resize'));

  $("#deriveDICOM").click(function() {
    downloadDatasets();
  });

  var $drawEraseButton = $('#drawErase');
  $drawEraseButton.click(function () {
    var configuration = cornerstoneTools.brush.getConfiguration();
    if (configuration.draw === 0) {
      configuration.draw = 1;
      $drawEraseButton.text("Erase");
    } else {
      configuration.draw = 0;
      $drawEraseButton.text("Draw");
    }
    cornerstoneTools.brush.setConfiguration(configuration);
  });

  var $radiusSlider = $('#radiusSlider');
  function setBrushRadius() {
    var configuration = cornerstoneTools.brush.getConfiguration();
    var radius = $radiusSlider.val();
    $('#valBox').text(radius);
    configuration.radius = radius;
    cornerstoneTools.brush.setConfiguration(configuration);
  }
  $radiusSlider.on('input', setBrushRadius);

  function handleFileDrop(e) {
    let evt = e.originalEvent;
    evt.stopPropagation();
    evt.preventDefault();

    resetDICOMzero();
    dc0.dataTransfer = {files: []};
    for (let fileIndex = 0; fileIndex < evt.dataTransfer.files.length; fileIndex++) {
      dc0.dataTransfer.files[fileIndex] = evt.dataTransfer.files[fileIndex];
    }

    status(`Got ${dc0.dataTransfer.files.length} files.  Processing...`);
    dc0.readOneFile(drawDatasets);
  }


  function GetGambar(id){
    $.ajax({url: "http://127.0.0.1/api/"+id, success: function(result){
      if(result.frame_images_count>1){
        drawSampleDatasets2(result.file_name);
      }
      else{
          window.location="http://127.0.0.1/viewsingle/"+id;
      }
        //downloadAndView("dicomweb:"+"http://127.0.0.1/uploads/"+result.file_name);
  //urls="dicomweb:http://127.0.0.1/uploads/"+result.file_name;
      //loadAndViewImage(urls);
     }});
  }
  
 
  GetGambar(id_image);

  $('#dropZone').bind('drop', handleFileDrop);
  $("#save").click(function(){
      var filename = document.getElementById('filename').value;
      alert(filename);
      cornerstoneTools.saveAs(element, filename);
      return false;
  });