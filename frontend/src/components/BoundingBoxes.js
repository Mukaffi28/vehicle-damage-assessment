import React, { useMemo, useRef, useState, useEffect } from 'react';
import './BoundingBoxes.css';

export default function BoundingBoxes({ imageSrc, bboxes = [] }) {
  const imgRef = useRef(null);
  const [dims, setDims] = useState({ naturalWidth: 1, naturalHeight: 1, clientWidth: 1, clientHeight: 1 });

  const onLoad = () => {
    const img = imgRef.current;
    if (!img) return;
    setDims({
      naturalWidth: img.naturalWidth || 1,
      naturalHeight: img.naturalHeight || 1,
      clientWidth: img.clientWidth || 1,
      clientHeight: img.clientHeight || 1,
    });
  };

  useEffect(() => {
    const img = imgRef.current;
    if (!img) return;
    const ro = new ResizeObserver(() => onLoad());
    ro.observe(img);
    return () => ro.disconnect();
  }, []);

  const scaledBoxes = useMemo(() => {
    const scaleX = dims.clientWidth / dims.naturalWidth;
    const scaleY = dims.clientHeight / dims.naturalHeight;
    return (bboxes || []).map((b, i) => ({
      left: Math.round(b.x * scaleX),
      top: Math.round(b.y * scaleY),
      width: Math.round(b.width * scaleX),
      height: Math.round(b.height * scaleY),
      key: i,
    }));
  }, [bboxes, dims]);

  return (
    <div className="bbox-wrapper">
      <img ref={imgRef} src={imageSrc} alt="Selected vehicle" className="preview-image" onLoad={onLoad} />
      {scaledBoxes.map((b) => (
        <div
          key={b.key}
          className="bbox-rect"
          style={{ left: b.left, top: b.top, width: b.width, height: b.height }}
        />
      ))}
    </div>
  );
}
