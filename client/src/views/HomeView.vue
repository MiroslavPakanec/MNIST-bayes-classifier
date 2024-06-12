<template>
  <div id="container" :style="{ background: gradient }" >
    <div id="navbar" :style="{'width': `${canvasWidth}px`, 'marginTop': `${marginTop}px`}">
      <button class="btn" @click="pixelStore.reset()">Reset</button>
      <button class="btn">Predict</button>
      <span id="prediction"></span>
    </div>
    <div id="canvas" :style="{ 'height': `${canvasHeight}px`, 'width': `${canvasWidth}px` }" />
  </div>
</template>

<script lang="ts" setup>
import p5 from 'p5'
import { ComputedRef, Ref, computed, onMounted, ref } from 'vue'
import { usePixelStore } from '@/stores/pixelStore'

const pixelStore = usePixelStore()
const brushDiameter: Ref<number> = ref(60)
const canvasPercent: Ref<number> = ref(0.6)
const canvasWidth: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const canvasHeight: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const marginTop: ComputedRef<number> = computed(() => (window.innerHeight / 2) - (canvasHeight.value / 2))

const isLmbPressed: Ref<boolean> = ref(false)
const mouseXPercent: Ref<number> = ref(0)
const mouseYPercent: Ref<number> = ref(0)
const gradient: ComputedRef<string> = computed(() => `radial-gradient(at ${mouseXPercent.value}% ${mouseYPercent.value}%, #3498db, #9b59b6)`)

const getMouseX = (sketch: any): number => sketch.mouseX - (canvasWidth.value / 2)
const getMouseY = (sketch: any): number => sketch.mouseY - (canvasHeight.value / 2)

const skipRender = (sketch: any): boolean => {
  const r: number = brushDiameter.value / 2
  if (sketch.mouseX - r >= canvasWidth.value) return true
  if (sketch.mouseX + r <= 0) return true
  if (sketch.mouseY - r >= canvasHeight.value) return true
  if (sketch.mouseY + r <= 0) return true
  return false
}

const drawCursor = (sketch: any): void => {
  sketch.strokeWeight = 1
  sketch.fill(255,255,255)
  sketch.ellipse(getMouseX(sketch), getMouseY(sketch), brushDiameter.value, brushDiameter.value)
}

const drawPixels = (sketch: any): void => {
  sketch.stroke(150, 150, 150)
  sketch.strokeWeight = 1
  for (let i = 0; i < pixelStore.pixels.length; i++) {
    const row = pixelStore.pixels[i]
    for (let j = 0; j < row.length; j++) {
      const pixel: number = row[j]
      sketch.fill(pixel, pixel, pixel)
      const w: number = canvasWidth.value / 28
      const h: number = w
      const x: number = (w * i) - (canvasHeight.value / 2)
      const y: number = (h * j) - (canvasHeight.value / 2)
      sketch.rect(x, y, w, h)
    }
  }
}

const sketch = (sketch: any) => {
  sketch.setup = () => {
    sketch.createCanvas(canvasWidth.value, canvasHeight.value, sketch.WEBGL)
    pixelStore.reset()
  }

  sketch.windowResized = () => {
    canvasWidth.value = window.innerHeight * canvasPercent.value
    canvasHeight.value = window.innerHeight * canvasPercent.value
  }

  sketch.draw = () => {
    if (skipRender(sketch)) return
    if (isLmbPressed.value) pixelStore.draw(sketch.mouseX, sketch.mouseY, brushDiameter.value, canvasWidth.value)
    sketch.background(255,255,255)
    drawPixels(sketch)
    drawCursor(sketch)
  }

  sketch.mousePressed = () => {
    if (sketch.mouseButton === sketch.LEFT) isLmbPressed.value = true
  }

  sketch.mouseReleased = () => {
    if (sketch.mouseButton === sketch.LEFT) isLmbPressed.value = false
  }

  sketch.mouseMoved = () => {
    mouseXPercent.value = clamp(0, sketch.mouseX / canvasWidth.value, 1) * 100
    mouseYPercent.value = clamp(0, sketch.mouseY / canvasHeight.value, 1) * 100
  }
}

const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)

onMounted(() => {
  const sketch_element = document.getElementById('canvas')
  if (sketch_element === null) return
  new p5(sketch, sketch_element)
})
</script>

<style scoped>
#container {
  height: 100vh;
  width: 100vw;
  overflow-x: hidden;
  background: rgb(155, 89, 182);
  background: radial-gradient(at center, rgb(51, 152, 219), #9b59b6);
}

#canvas {
  padding: 10px;
  background-color: rgba(255,255,255, 1);
  border-radius: 20px;
  border: 1px solid rgb(51, 152, 219);
  margin: auto;
  cursor: none;
}

#navbar {
  margin: auto;
  margin-bottom: 10px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 5px;
  /* border: 1px solid white;
  border-radius: 20px; */
  gap: 10px;
}

.btn {
  padding: 10px;
  border: 1px solid white;
  background-color: transparent;
  color: white;
  border-radius: 5px;
}

.btn:hover {
  cursor: pointer;
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(219, 128, 255, 0.2);
}

.btn.active {
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(219, 128, 255, 0.2)
}


</style>
