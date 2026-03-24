<template>
  <div class="section" id="gallery">
    <div class="gallery-header">
        <h1 class="gallery-title">PATTERN</h1>
        <div class="search-container" v-if="searchedTerm">
            <p class="bold searchTermTitle">Searched Word(s)</p>
            <div class="searchTerm" id="searchTermGallery">{{ searchedTerm }}</div>
        </div>

        <div class="relatedWordsContainer" v-if="semanticSearch && semanticSearch.length">
          <p class="bold relatedWordsTitle">Related Words List</p>
          <div class="relatedWords" id="relatedWordsGallery">{{ semanticSearch.join(", ") }}</div>
        </div>
    </div>
    <div class="warning"></div>
    <div class="container-unit">
      <aside class="left-menu">
        <h2>LIBRARY</h2>
        <div class="images-container" id="elements-images">
          <div class="libray">
            <div v-for="(unit, index) in library_unit" 
            :key="index" 
            class="library-item"
            :class="{ selected: isSelected(unit) }"
            @click="toggleSelection(unit)">
              <canvas
                ref="libraryCanvas"
                :data-index="index" 
                width="345"
                height="345"
                class="sketch-thumbnail"
              ></canvas>
            </div>
          </div>
        </div>

        <div class="sketches">
          <h2>SKETCHES</h2>
          <div class="sketch-grid">
            <div v-for="(sketch, index) in sketches" :key="index" class="sketch-item">
              <canvas
                :ref="'sketchesCanvas' + index"
                width="345"
                height="345"
                class="sketch-thumbnail"
              ></canvas>
            </div>
          </div>
        </div>
      </aside>
    <main class="display-area">
      <div v-if="showPopup == true" class="popup-overlay">
        <div class="popup-content">
          <img :src="`http://127.0.0.1:5000/backend/static/expand_pattern/my_custom_pattern.png?t=${new Date().getTime()}`" alt="Expanded Pattern" />
          <button @click="closePopup">×</button>
        </div>
      </div>
      <div class="first-displayarea">
      <div class="bottom-icons">
        <button @click="toggleSlider" class="color" title="Change Background Color">
          <span class="dropdown-arrow">▲</span>
          <div
            class="color-circle"
            :style="{ backgroundColor: selectedColor }"
          ></div>
        </button>
        <button @click="cleanCanvas" class="clean" title="clean"><img alt="clean" src="static/icons/clean.png"/></button>
        <button @click="undo" :disabled="undoStack.length === 0" class="undo"><img alt="undo" src="static/icons/undo.png"/></button>
        <button @click="redo" :disabled="redoStack.length === 0" class="redo"><img alt="redo" src="static/icons/redo.png"/></button>
        <button @click="expand" class="expand" title="Expand"><img alt="expand" src="static/icons/expand.png"/></button>
        <button @click="export_sketch" class="export" title="Export"><img alt="export" src="static/icons/export.png"/></button>
        
        <div v-if="showSlider" class="slider-container">
            <input
              type="range"
              min="0"
              max="360"
              v-model="hue"
              @input="updateBackgroundCanvas"
              @change="finalizeColorChange"
              class="color-slider"
            />
            <div
              class="color-preview"
              :style="{ backgroundColor: selectedColor }"
            >
          </div>
        </div>
      </div>
      
      
      <div class="canvas">
        <canvas ref="canvas" width="345" height="345"></canvas>
      </div>
      <div v-if="selectedItem !== null" class="opacity-slider">
          <label for="opacity">OPACITY:</label>
          <input
            id="opacity"
            type="range"
            min="0.2"
            max="1"
            step="0.01"
            v-model.number="tranparencyLevel"
            @input="updateCanvasTransparency(selectedItem)"          
            @change="finalizeTransparencyChange"

          />
        </div>
    </div>
    
      <div class="graph-container" id="principles-graph">
        <svg
          height="254"
          width="254"
          viewBox="0 0 254 254"
          xmlns="http://www.w3.org/2000/svg"
        >
          <line stroke="#A67E66" x1="127" x2="127" y1="127" y2="2"></line>
          <line stroke="#A67E66" x1="127" x2="2" y1="127" y2="189.5"></line>
          <line stroke="#A67E66" x1="127" x2="250" y1="127" y2="189.5"></line>

          <polygon
            fill="#A67E66"
            fill-opacity="0.05"
            points="127,2 127,127 2,189.5 2,64.5"
          ></polygon>

          <polygon
            fill="#A67E66"
            fill-opacity="0.05"
            points="127,2 127,127 250,189.5 250,64.5"
          ></polygon>

          <polygon
            fill="#A67E66"
            fill-opacity="0.05"
            points="2,189.5 127,127 250,189.5 127,250"
          ></polygon>

          <text data-v-53feb1c5="" fill="#A67E66" font-size="10" transform="rotate(90, 127, 64)" x="73" y="79"> 
            TRANSPARENCY
          </text>
          <text fill="#A67E66" font-size="10" transform="rotate(-26, 2, 183)" x="8" y="183">
            HUE
          </text>
          <text fill="#A67E66" font-size="10" transform="rotate(90, 127, 64)" x="73" y="58">            
            CONCENTRATION
          </text>
          <text fill="#A67E66" font-size="10" transform="rotate(26.5, 193, 175)" x="205" y="175">
            SCALE
          </text>
          <text fill="#A67E66" font-size="10" transform="rotate(26.5, 190, 154)" x="218" y="154">
            SPACE
          </text>
          <text fill="#A67E66" font-size="10" transform="rotate(-26, 7, 201)" x="19" y="201">
            MOTION
          </text>

          <circle
            v-for="(point, index) in points"
            :key="index"
            class="draggable"
            :cx="point.x"
            :cy="point.y"
            r="4"
            fill="#000"
          ></circle>

          <polygon
            fill="#A67E66"
            fill-opacity="0.2"
            :points="trianglePoints"
          ></polygon>
        </svg>
      </div>
    </main>
    <aside class="right-menu">
      <div class="principles">
        <h2>CONTRIBUTIONS</h2>
        <div class="images-container-left">
          <p class="principles-caption">WHAT THE COMPUTER WILL CONTRIBUTE</p>
          <div class="buttons-container">
            <button v-for="(principle, index) in principles" 
            :key="index"
            class="principle-button"
            :style="{
              gridColumn: principle.gridColumn,
              gridRow: principle.gridRow,
              backgroundColor: principle.selected ? '#A67E66' : '#F9F5EF',
              color: principle.selected ? 'white' : 'black'
            }"
            @click="toggleSelectionPrinciples(index)">
              {{ principle.name }}
            </button>
          </div>
          <div class="change-section">
            <button 
              :disabled="!anySelected" 
              @click="principlesContributions()" 
              class="check-mark"
              :class="{ disabled: !anySelected }"
            >
              APPLY
            </button>
          </div>
          <div class="explainable-container" v-if="messagesToShow.length > 0">
            <p class="principles-caption">WHAT THE COMPUTER WILL CHANGE</p>
          </div>
          <div class="justification-message">
            <div v-for="(message, index) in messagesToShow" :key="index" class="message-item">
              <p v-html="message.text"></p>
            </div>
          </div>
        </div>
        
      </div>
    
    <div class="suggestions">
      <h2>SUGGESTIONS</h2>
      <div class="suggestion-grid">
        <div v-for="(suggestion, index) in suggestions" :key="index" class="suggestion-item">
          <canvas
            :ref="'suggestionCanvas' + index"
            width="345"
            height="345"
            class="suggestion-thumbnail"
          ></canvas>
          <button @click="acceptSuggestion(index)" 
          class="check-mark"
          style="margin-top: 0.4rem; font-size: 10px;"
          >SELECT</button>
        </div>
      </div>
    </div>

    </aside>
  </div>
    <div class="footerpattern">
        <div class="navigation">
          <span class="nav-circle"></span>
          <span class="nav-line"></span>
          <span class="nav-circle"></span>
          <span class="nav-line"></span>
          <span class="nav-circle"></span>
          <span class="nav-line"></span>
          <span class="nav-circle active"></span>
        </div>
        <div class="navigation-names">
          <span class="nav">GALLERY</span>
          <span class="nav">SELECTED GALLERY</span>
          <span class="nav">UNIT DEVELOPMENT</span>
          <span class="nav active">PATTERN</span>
        </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: "UnitDevelopment",
  data() {
    return {
      sketches: [],
      library: [],
      library_unit: [],
      suggestions: [],
      principles: [
        { name: "ELEMENTS", gridColumn: 1, gridRow: 1, selected: false},
        { name: "HUE", gridColumn: 1, gridRow: 2, selected: false },
        { name: "TRANSPARENCY", gridColumn: 2, gridRow: 2, selected: false },
        { name: "MOTION", gridColumn: 3, gridRow: 2, selected: false },
        { name: "SCALE", gridColumn: 1, gridRow: 3, selected: false },
        { name: "SPACE", gridColumn: 2, gridRow: 3, selected: false },
        { name: "CONCENTRATION", gridColumn: 3, gridRow: 3, selected: false },
      ],      
      selectedItem: null, 
      points: [],
      draggingPointIndex: null, 
      solutions: [],
      images: [],
      showSlider: false, 
      hue: 0, 
      selectedColor: "FFFFFF", 
      undoStack: [], 
      redoStack: [],
      transparency: 127,
      value: 0,
      motion: 127,
      scale: 254,
      concentration: 1,
      space: 230,
      message: "",
      angle_value: 0,
      angle_space: 0,
      messagesToShow: [],
      firstLoad: true,
      previousStates: [],
      newState: [],
      interacting: false,
      tranparencyLevel: 0,
      counterUndo: 0,
      counterRedo: 0,
      expandPath: "",
      showPopup: false,
      decomposed_info: [],
      library_names: [],
      hoveredInfo: null,
      structureTypeThresholds: [
        [0, 0.125],    
        [0.125, 0.25], 
        [0.25, 0.375], 
        [0.375, 0.50], 
        [0.50, 0.625], 
        [0.625, 0.75], 
        [0.75, 0.875], 
        [0.875, 1]     
      ],
      group1: [0, 2, 5, 7, 8, 10, 13, 15],
      group1_1: [1, 3, 4, 6, 7, 9, 11, 14],
      group2: [1, 3, 4, 6, 9, 11, 12, 14],
      group2_1: [0, 2, 5, 7, 8, 10, 13, 15],
      group3: [0, 1, 2, 3, 8, 9, 10, 11],
      group3_1: [4, 5, 6, 7, 12, 13, 14, 15],
      group4: [0, 2, 4, 6, 8, 10, 12, 14],
      group4_1: [1, 3, 5, 7, 9, 11, 13, 15],
    };
  },
  mounted() {
    const units = this.$route.query.sketches ? JSON.parse(this.$route.query.sketches) : [];
    this.library_unit = units;
    this.concentration = Math.floor(Math.random() * (127 - 120 + 1)) + 120;
    this.transparency = Math.floor(Math.random() * (127 - 120 + 1)) + 120;
    this.motion = Math.floor(Math.random() * (127 - 0 + 1)) + 0;
    this.scale = Math.floor(Math.random() * (254 - 200 + 1)) + 200;
    this.space = Math.floor(Math.random() * (200 - 140 + 1)) + 140;
    this.selectImage();
    this.startSystem();
  },
  computed: {
    trianglePoints() {
      return this.points.map((p) => `${p.x},${p.y}`).join(" ");
    },
    anySelected() {
      return this.principles.some(principle => principle.selected);
    }
  },
  created() {
    this.points = [
        { x: this.value, y: this.transparency }, 
        { x: this.motion, y: this.scale },       
        { x: this.space, y: this.concentration } 
      ];
  },
  methods: {
    async selectImage() {
      const randomIndex = Math.floor(Math.random() * this.library_unit.length);
      this.solutions.push(randomIndex);
    },
    async loadImages() {
      this.previousStates = [];
      this.newState = [];
      this.firstLoad = true;
      this.images = []; 

      this.message = "";
      this.angle_value = 0;
      this.angle_space = 0;
      this.messagesToShow = [];
      this.interacting = false;

      const imagePaths = this.solutions.map(index => `/static/final_unit/sketch_${index}.png`);

      const imagePromises = imagePaths.map((path, imgIndex) => {
        return new Promise((resolve, reject) => {
          const img = new Image();
          img.src = `${path}?t=${new Date().getTime()}`;

          img.onload = () => {
            const canvasWidth = this.$refs.canvas.width;
            const canvasHeight = this.$refs.canvas.height;

            const cellWidth = canvasWidth / 4; 
            const cellHeight = canvasHeight / 4; 

            const group = this.library_unit[this.solutions[imgIndex]] || [];
            const backgroundColor = group[0]?.backgroundColor || '#ffffff'; 
            this.selectedColor = backgroundColor;
            if (this.selectedColor == "#FFFFFF" ) {
              this.hue = 360;
              this.selectedColor == "#FFFFFF";
            }
            else if (this.selectedColor == "#000000") {
              this.hue = 0 ;
              this.selectedColor == "#000000"
            } else {
              const match = backgroundColor.match(/hsl\(([\d.]+),/);
              this.hue = parseFloat(match[1]);
            }

            this.value = this.mappingValue();
            this.updatePoints();
            for (let gridRow = 0; gridRow < 4; gridRow++) {
              for (let gridCol = 0; gridCol < 4; gridCol++) {
                this.images.push({
                  id: gridRow * 4 + gridCol + imgIndex * 16, 
                  image: img,
                  src: img.src,
                  x: gridCol * cellWidth,
                  y: gridRow * cellHeight,
                  width: cellWidth,
                  height: cellHeight,
                  originalWidth: img.width,
                  originalHeight: img.height,
                  rotation: 0,
                  opacity: 1,
                  backgroundColor: backgroundColor,
                });
              }
            }
            resolve();
          };
          
          img.onerror = (error) => reject(error);
        });
      });

      try {
        await Promise.all(imagePromises);
      } catch (error) {
        console.error("Error loading images:", error);
      }
    },

    async startSystem() {
      this.drawLibrary();

      const canvas = this.$refs.canvas;
      if (!canvas) {
        console.error("Canvas element not found!");
        return;
      }

      const ctx = canvas.getContext("2d");

      if (!ctx) {
          console.error("Failed to get 2D context");
          return;
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    
      await this.loadImages();
      this.images = await this.generateAndSelectBestSolution();
      
      this.drawImages(ctx);
      
      this.drawSuggestions();

      this.setupCanvasInteraction(canvas);
      this.firstLoad = false;
    },
 
    setupCanvasInteraction(canvas) {
        canvas.addEventListener("mousedown", this.startInteraction);
        canvas.addEventListener("mousemove", this.interact);
        canvas.addEventListener("mouseup", this.stopInteraction);        
    },

    async generateAndSelectBestSolution() {
      if (!this.firstLoad){
        this.saveState();
      }

      let numberOfSolutions = 0;
        if (this.interacting){
          numberOfSolutions = 20;
        } else {
          numberOfSolutions = 20;
        }
        let bestSolution = null;
        let rankedSolutions = [];

        for (let i = 0; i < numberOfSolutions; i++) {
            this.applyPrinciplesToCanvas();
            const score = this.evaluateSolution();
            const solutionState = this.cloneCanvasState();
            rankedSolutions.push({ score, state: solutionState });
        }
        rankedSolutions.sort((a, b) => b.score - a.score);
        if (this.interacting){
          bestSolution = this.newState;
          this.suggestions = rankedSolutions.slice(0, 3).map((item) => item.state);
        } else {
          bestSolution = rankedSolutions[0]?.state;
          this.suggestions = rankedSolutions.slice(1, 4).map((item) => item.state);
        }
        return bestSolution;
    },

    applyPrinciplesToCanvas() {
      if (this.firstLoad){
        this.inverseMappingScale(this.scale);
        this.inverseMappingMotion(this.motion);
        this.inverseMappingTransparency(this.transparency);
        this.inverseMappingValue(this.value);
        this.inverseMappingConcentration(this.concentration);
        this.inverseMappingSpace(this.space);
      } if (this.interacting){
        this.inverseMappingScale(this.scale);
        this.inverseMappingMotion(this.motion);
        this.inverseMappingTransparency(this.transparency);
        this.inverseMappingValue(this.value);
        this.inverseMappingConcentration(this.concentration);
        this.inverseMappingSpace(this.space);
      }else {
        this.principles.forEach(principle => {
          if (principle.selected) {
            switch (principle.name) {
              case "SCALE":
                this.inverseMappingScale(this.scale);
                break;
              case "MOTION":
                this.inverseMappingMotion(this.motion);
                break;
              case "TRANSPARENCY":
                this.inverseMappingTransparency(this.transparency);
                break;
              case "HUE":
                this.inverseMappingValue(this.value);
                break;
              case "CONCENTRATION":
                this.inverseMappingConcentration(this.concentration);
                break;
              case "SPACE":
                this.inverseMappingSpace(this.space);
                break;
              case "ELEMENTS":
                this.inverseMappingSpace(this.space);
                this.inverseMappingConcentration(this.concentration);
                this.inverseMappingScale(this.scale);
                break;
              default:
                console.warn(`Unknown principle: ${principle.name}`);
            }
          }
        });
      }

    },

    inverseMappingValue(targetValue) {
      const minValue = 0;   
      const maxValue = 127;

      const originalHue = this.mapValue(
        targetValue,
        minValue,
        maxValue,
        0,
        360
      );

      this.hue = originalHue;
      if (this.hue == 360) {
        this.selectedColor = "#FFFFFF";
      }
      else if (this.hue == 0) {
        this.selectedColor = "#000000";
      }
      else {
        this.selectedColor = `hsl(${this.hue}, 60%, 50%)`;
      }
      this.images.forEach((image) => {
        image.backgroundColor = this.selectedColor;
      });
    },

    inverseMappingTransparency(targetTransparency) {

      this.images.forEach((image) => {
        image.opacity = 1; 
      });

      const minTransparency = 0;
      const maxTransparency = 127;

      const averageOpacity = this.mapValue(
        targetTransparency,
        minTransparency,
        maxTransparency,
        0.2,
        1
      );


      const imageCount = this.images.length;
      if (imageCount === 0) {
        console.warn("Nenhuma imagem disponível para ajustar opacidade.");
        return;
      }

      if (averageOpacity === 1) {
        this.images.forEach((image) => {
          image.opacity = 1;
        });
        return;
      } else if (averageOpacity === 0.2) {
        this.images.forEach((image) => {
          image.opacity = 0.2; 
        });
        return;
      }

      let group = [];
      let inverseGroup = [];
      const randomIndex = Math.floor(Math.random() * this.images.length);
      const selectedImage = this.images[randomIndex];

      if (selectedImage.id === 0) {
        group = this.group3;
        inverseGroup = this.group3_1;
      } else if (selectedImage.id === 1) {
        group = this.group2;
        inverseGroup = this.group2_1;
      } else if (selectedImage.id === 4) {
        group = this.group4;
        inverseGroup = this.group4_1;
      } else if (selectedImage.id === 12) {
        group = this.group3_1;
        inverseGroup = this.group3;
      } else {
        group = this.group1.includes(this.selectedItem) ? this.group1 : this.group2;
        inverseGroup = group === this.group1 ? this.group1_1 : this.group2_1;
      }

      let randomGroup = Math.random() * (1 - 0.2) + 0.2;
      let randomInverseGroup = Math.random() * (1 - 0.2) + 0.2;
      let currentAverageOpacity = 0;
      group.forEach((index) => {
        const image = this.images[index];
        image.opacity = randomGroup; 
        currentAverageOpacity += image.opacity;
      });

      inverseGroup.forEach((index) => {
        const image = this.images[index];
        image.opacity = randomInverseGroup; 
        currentAverageOpacity += image.opacity;
      });

      const adjustmentThreshold = 0.01; 
      const adjustmentStep = 0.01;      
      let iteration = 0;

      while (
        Math.abs(currentAverageOpacity / imageCount - averageOpacity) > adjustmentThreshold &&
        iteration < 1000
      ) {
        iteration++;

        if (currentAverageOpacity / imageCount < averageOpacity) {
          inverseGroup.forEach((index) => {
            const image = this.images[index];
            if (image.opacity < 1) {
              image.opacity = Math.min(image.opacity + adjustmentStep, 1);
              currentAverageOpacity += adjustmentStep / imageCount;
            }
          });
        } else {
          group.forEach((index) => {
            const image = this.images[index];
            if (image.opacity > 0.2) {
              image.opacity = Math.max(image.opacity - adjustmentStep, 0.2);
              currentAverageOpacity -= adjustmentStep / imageCount;
            }
          });
        }
      }
    },

    inverseMappingMotion(targetMotion) {
      const minMotion = 127;   
      const maxMotion = 0;    
      const maxRotation = Math.PI; 

      const targetAverageDeviation = this.mapValue(
        targetMotion,
        minMotion,
        maxMotion,
        0,  
        1   
      );

      let group = [];
      let inverseGroup = [];

      const randomIndex = Math.floor(Math.random() * this.images.length);
      const selectedImage = this.images[randomIndex];

      if (selectedImage.id == 0) {
          group = this.group3;
          inverseGroup = this.group3_1;
      } else if (selectedImage.id == 1) {
          group = this.group2;
          inverseGroup = this.group2_1;
      } else if (selectedImage.id == 4) {
          group = this.group4;
          inverseGroup = this.group4_1;
      } else if (selectedImage.id === 12) {
        group = this.group3_1;
        inverseGroup = this.group3;
      } else {
          group = this.group1.includes(this.selectedItem) ? this.group1 : this.group2;
          inverseGroup = group === this.group1 ? this.group1_1 : this.group2_1;
      }

      const requiredTotalDeviation = targetAverageDeviation * this.images.length;

      let currentTotalDeviation = 0;

      const deviations = []; 
      const randomFactor = Math.random(); 

      group.forEach((index) => {
        const image = this.images[index];
        const initialDeviation = targetAverageDeviation * randomFactor * maxRotation;
        image.rotation = randomFactor < 0.5 ? -initialDeviation : initialDeviation;
        
        const normalizedRotation = Math.abs(image.rotation) % (2 * Math.PI);
        const deviation = Math.min(normalizedRotation, 2 * Math.PI - normalizedRotation);
        deviations.push(deviation);
        currentTotalDeviation += deviation / maxRotation;
      });

      let iteration = 0;
      const adjustmentStep = 0.01 * maxRotation; 

      while (
        Math.abs(currentTotalDeviation - requiredTotalDeviation) > 0.01 &&
        iteration < 1000
      ) {
        iteration++;
        let adjustGroup = iteration % 2 === 0 ? group : inverseGroup; 
        adjustGroup.forEach((index) => {
            const image = this.images[index];
            if (currentTotalDeviation < requiredTotalDeviation) {
              image.rotation += adjustmentStep;
            } else {
              image.rotation -= adjustmentStep;
            }

            const newRotation = Math.abs(image.rotation) % (2 * Math.PI);
            const newDeviation = Math.min(newRotation, 2 * Math.PI - newRotation);
            deviations[index] = newDeviation;
            currentTotalDeviation += newDeviation / maxRotation;
          });
        }
    },

    inverseMappingScale(targetScale) {
      const minScale = 127;    
      const maxScale = 252;    
      const maxDifference = 1; 

      let targetAverageDifference = this.mapValue(
        targetScale,
        maxScale,
        minScale,
        0,            
        maxDifference 
      );
      targetAverageDifference = Math.max(0, Math.min(targetAverageDifference, maxDifference));

      let group = [];
      let inverseGroup = [];

      const randomIndex = Math.floor(Math.random() * this.images.length);
      const selectedImage = this.images[randomIndex];

      if (selectedImage.id === 0) {
        group = this.group3;
        inverseGroup = this.group3_1;
      } else if (selectedImage.id === 1) {
        group = this.group2;
        inverseGroup = this.group2_1;
      } else if (selectedImage.id === 4) {
        group = this.group4;
        inverseGroup = this.group4_1;
      } else if (selectedImage.id === 12) {
        group = this.group3_1;
        inverseGroup = this.group3;
      } else {
        group = this.group1.includes(this.selectedItem) ? this.group1 : this.group2;
        inverseGroup = group === this.group1 ? this.group1_1 : this.group2_1;
      }

      group.forEach((index) => {
        const image = this.images[index];
        image.width = image.originalWidth / 4;
        image.height = image.originalHeight / 4;

      });

      let iteration = 0;
      const adjustmentStep = 0.5; 
      let currentAverageDifference = 0;

      if (targetAverageDifference === 0){
        inverseGroup.forEach((index) => {
        const image = this.images[index];
        image.width = image.originalWidth / 4;
        image.height = image.originalHeight / 4;
      });
      } else {
          while (iteration < 1000) {
            iteration++;

            let totalRelativeDifference = 0;
            let pairCount = 0;

            inverseGroup.forEach((index, i) => {
              const inverseImage = this.images[index];
              const referenceImage = this.images[group[i % group.length]];

              const originalRatio = referenceImage.originalWidth / inverseImage.originalWidth;
              const currentRatio = referenceImage.width / inverseImage.width;
              const relativeDifference = Math.abs(Math.log(currentRatio / originalRatio));

              totalRelativeDifference += relativeDifference;
              pairCount++;

              if (relativeDifference < targetAverageDifference) {
                inverseImage.width += adjustmentStep;
                inverseImage.height = inverseImage.width * (inverseImage.originalHeight / inverseImage.originalWidth);
              } else {
                inverseImage.width -= adjustmentStep;
                inverseImage.height = inverseImage.width * (inverseImage.originalHeight / inverseImage.originalWidth);
              }

              inverseImage.width = Math.max(30, Math.min(inverseImage.width, 200));
              inverseImage.height = Math.max(30, Math.min(inverseImage.height, 200));
            });

            currentAverageDifference = totalRelativeDifference / pairCount;

            if (Math.abs(currentAverageDifference - targetAverageDifference) < 0.001) {
              break;
            }
          }
          inverseGroup.forEach((index) => {
            const inverseImage = this.images[index];
            inverseImage.width = Math.max(inverseImage.width, 1);
            inverseImage.height = Math.max(inverseImage.height, 1);
          });
        }
    },

    ensureWithinCanvas(image, canvas) {
      image.x = Math.max(0, Math.min(image.x, canvas.width - image.width));
      image.y = Math.max(0, Math.min(image.y, canvas.height - image.height));
    },

    adjustElementsToCanvas() {
      const canvas = this.$refs.canvas;
      if (!canvas) {
        console.error("Canvas not found!");
        return;
      }
      this.images.forEach(image => this.ensureWithinCanvas(image, canvas));
    },

    inverseMappingConcentration(targetConcentration) {
      const canvas = this.$refs.canvas;
      if (!canvas) {
        console.error("Canvas element not found!");
        return;
      }

      const cellWidth = canvas.width / 4; 
      const cellHeight = canvas.height / 4; 

      let group = [];
      let inverseGroup = [];
      const randomIndex = Math.floor(Math.random() * this.images.length);
      const selectedImage = this.images[randomIndex];

      if (selectedImage.id === 0) {
        group = this.group3;
        inverseGroup = this.group3_1;
      } else if (selectedImage.id === 1) {
        group = this.group2;
        inverseGroup = this.group2_1;
      } else if (selectedImage.id === 4) {
        group = this.group4;
        inverseGroup = this.group4_1;
      } else if (selectedImage.id === 12) {
        group = this.group3_1;
        inverseGroup = this.group3;
      }else {
        group = this.group1.includes(this.selectedItem) ? this.group1 : this.group2;
        inverseGroup = group === this.group1 ? this.group1_1 : this.group2_1;
      }

      const minDistance = 0; 
      const maxDistance = cellWidth; 
      const mappedMin = 127, mappedMax = 0;

      const targetDistance = this.mapValue(
            targetConcentration, mappedMin, mappedMax, maxDistance, minDistance
          );

      const resetPositions = () => {
        group.forEach((cellId) => {
          const element = this.images[cellId];
          const cellRow = Math.floor(cellId / 4);
          const cellCol = cellId % 4;
          element.x = cellCol * cellWidth;
          element.y = cellRow * cellHeight;
        });

        inverseGroup.forEach((cellId) => {
          const element = this.images[cellId];
          const cellRow = Math.floor(cellId / 4);
          const cellCol = cellId % 4;
          element.x = cellCol * cellWidth;
          element.y = cellRow * cellHeight;
        });
      };

      resetPositions();

    const positionGroups = () => {
      group.forEach((cellId, index) => {
        const element = this.images[cellId];
        const inverseElement = this.images[inverseGroup[index]];

        const cellRow = Math.floor(cellId / 4);
        const cellCol = cellId % 4;
        const cellCenterX = cellCol * cellWidth + cellWidth / 2;
        const cellCenterY = cellRow * cellHeight + cellHeight / 2;

        const inverseCellId = inverseGroup[index];
        const inverseCellRow = Math.floor(inverseCellId / 4);
        const inverseCellCol = inverseCellId % 4;
        const inverseCellCenterX = inverseCellCol * cellWidth + cellWidth / 2;
        const inverseCellCenterY = inverseCellRow * cellHeight + cellHeight / 2;

        const directionX = inverseCellCenterX - cellCenterX;
        const directionY = inverseCellCenterY - cellCenterY;
        const distance = Math.sqrt(directionX ** 2 + directionY ** 2);

        const normalizedX = directionX / distance || 0; 
        const normalizedY = directionY / distance || 0;

        const offsetX = normalizedX * targetDistance;
        const offsetY = normalizedY * targetDistance;

        element.x = cellCenterX - element.width / 2;
        element.y = cellCenterY - element.height / 2;

        inverseElement.x = cellCenterX + offsetX - inverseElement.width / 2;
        inverseElement.y = cellCenterY + offsetY - inverseElement.height / 2;
      });
    };
      positionGroups();

    },

    inverseMappingSpace(targetSpace) {
      const canvas = this.$refs.canvas;
      const canvasArea = canvas.width * canvas.height;

      let emptySpaceScore = this.mapValue(targetSpace, 127, 254, 0, 1);
      const mappedConcentration = this.mapValue(this.concentration, 127, 0, 0, 1);

      let targetOccupationRatio =
            1 - emptySpaceScore - (1 - mappedConcentration) * 0.3;

      if (targetOccupationRatio < 0 || targetOccupationRatio > 1) {        
        targetOccupationRatio = Math.max(0.05, Math.min(targetOccupationRatio, 0.95));
      }


      const targetEffectiveArea = targetOccupationRatio * canvasArea;
      let totalEffectivePixels = 0;

      for (const image of this.images) {
            const effectivePixels = this.calculateEffectiveArea(image, canvas);
            totalEffectivePixels += effectivePixels;
      }

      const scaleFactor = Math.sqrt(targetEffectiveArea / totalEffectivePixels);

      for (const image of this.images) {
        image.width *= scaleFactor;
        image.height *= scaleFactor;

        if (image.width < 30) {
          const aspectRatio = image.height / image.width; 
          image.width = 30;
          image.height = image.width * aspectRatio;
        }
        if (image.height < 30) {
          const aspectRatio = image.width / image.height; 
          image.height = 30;
          image.width = image.height * aspectRatio;
        }

      }
      this.space = targetSpace;
      this.updatePoints();
    },




    evaluateSolution() {
        let score = 0;

        score += this.evaluateAlignmentWithPrinciples();
        score += this.evaluateInteractionWithCorners();
        score += this.evaluateBackgroundColor();
        score += this.evaluateScale();
        score += this.evaluateConcentration();
        score += this.evaluateMotion();
        score += this.evaluateSpace();
        score += this.evaluateTransparency();

        return score;
    },

    cloneCanvasState() {
      if (!Array.isArray(this.images)) {
        console.error("Error: 'images' is not an array or is undefined.");
        return [];
      }

      return this.images.map(imageObj => ({
        ...imageObj,
        image: imageObj.image, 
      }));
    },

    cloneCanvasStateManual() {
      return JSON.parse(JSON.stringify(this.images.map((image) => ({
        x: image.x,
        y: image.y,
        width: image.width,
        height: image.height,
        rotation: image.rotation,
        opacity: image.opacity,
        backgroundColor: image.backgroundColor,
      }))));
    },

    applyCanvasState(state) {
        this.images = state.map(imageObj => {
            const img = new Image();
            img.src = imageObj.image; 
            return {
                ...imageObj,
                image: img, 
            };
        });
    },



    evaluateInteractionWithCorners() {
        const interactingElements = this.calculateCornerInteractions();
        const totalElements = this.images.length;
        const ratio = interactingElements / totalElements;

        if (ratio === 1) return 5;
        if (ratio >= 0.5) return 3;
        return 0;
    },

    calculateCornerInteractions() {
        return this.images.filter(image => {
            const nearLeft = image.x <= 10;
            const nearRight = image.x + image.width >= this.canvasWidth - 10;
            const nearTop = image.y <= 10;
            const nearBottom = image.y + image.height >= this.canvasHeight - 10;
            return nearLeft || nearRight || nearTop || nearBottom;
        }).length;
    },

    evaluateBackgroundColor() {
        const backgroundHSL = this.parseHSL(this.selectedColor);
        if (!backgroundHSL) {
            console.error("Invalid background color.");
            return 0;
        }

        const elementColors = this.getAllColorsFromElements();
        if (elementColors.length === 0) {
            console.error("No color detected in the elements.");
            return 0;
        }

        let isFullComplementary = false;
        let isPartialComplementary = false;

        for (const color of elementColors) {
            if (this.isComplementary(color, backgroundHSL) || this.isAdjacent(color, backgroundHSL)) {
                if (this.isPredominant(color)) {
                    isFullComplementary = true; 
                } else {
                    isPartialComplementary = true; 
                }
            }
        }

        if (isFullComplementary){
          return 5;
        }
        if (isPartialComplementary) {
          return 3;
        }
        return 0;
    },
    isComplementary(color1, color2) {
        const hueDifference = Math.abs(color1.hue - color2.hue);
        return hueDifference === 180 || hueDifference === 360;
    },
    isAdjacent(color1, color2) {
        const hueDifference = Math.abs(color1.hue - color2.hue);
        return hueDifference <= 30 || hueDifference >= 330;
    },
    isPredominant(color) {
        const predominantColor = this.predominantElementColor;
        return predominantColor &&
            color.hue === predominantColor.hue &&
            color.saturation === predominantColor.saturation &&
            color.lightness === predominantColor.lightness;
    },
    getAllColorsFromElements() {
        const colorSet = new Set();

        for (const imageObj of this.images) {
            const { image, width, height } = imageObj;

            if (!image || !width || !height) {
                console.error("Imagem inválida:", imageObj);
                continue;
            }

            const colors = this.calculateColorsFromImage(image, width, height);
            colors.forEach(color => colorSet.add(color));
        }

        return Array.from(colorSet).map(color => {
            const [r, g, b] = color.split(',').map(Number);
            return this.rgbToHSL(r, g, b);
        });
    },
    calculateColorsFromImage(image, width, height) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const colorFrequency = new Map();

        canvas.width = width;
        canvas.height = height;

        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(image, 0, 0, width, height);

        const imageData = ctx.getImageData(0, 0, width, height);
        const pixels = imageData.data;

        for (let i = 0; i < pixels.length; i += 4) {
            const r = pixels[i];
            const g = pixels[i + 1];
            const b = pixels[i + 2];
            const alpha = pixels[i + 3];

            if (alpha === 0) continue;

            const key = `${Math.round(r / 5) * 5},${Math.round(g / 5) * 5},${Math.round(b / 5) * 5}`;
            colorFrequency.set(key, (colorFrequency.get(key) || 0) + 1);
        }

        return Array.from(colorFrequency.keys());
    },
    parseHSL(color) {
        if (color.startsWith('hsl')) {
            const matches = color.match(/\d+(\.\d+)?/g);
            if (!matches || matches.length < 3) return null;

            return {
                hue: parseFloat(matches[0]),
                saturation: parseFloat(matches[1]),
                lightness: parseFloat(matches[2]),
            };
        } else if (color.startsWith('#')) {
            return this.hexToHSL(color);
        }
        return null;
    },
    hexToHSL(hex) {
        hex = hex.replace(/^#/, '');
        let r = parseInt(hex.slice(0, 2), 16) / 255;
        let g = parseInt(hex.slice(2, 4), 16) / 255;
        let b = parseInt(hex.slice(4, 6), 16) / 255;

        let max = Math.max(r, g, b), min = Math.min(r, g, b);
        let hue = 0, saturation = 0, lightness = (max + min) / 2;

        if (max !== min) {
            const delta = max - min;
            saturation = lightness > 0.5 ? delta / (2 - max - min) : delta / (max + min);
            switch (max) {
                case r: hue = ((g - b) / delta + (g < b ? 6 : 0)); break;
                case g: hue = ((b - r) / delta + 2); break;
                case b: hue = ((r - g) / delta + 4); break;
            }
            hue *= 60;
        }

        return {
            hue: Math.round(hue),
            saturation: Math.round(saturation * 100),
            lightness: Math.round(lightness * 100),
        };
    },
    rgbToHSL(r, g, b) {
        r /= 255;
        g /= 255;
        b /= 255;

        let max = Math.max(r, g, b), min = Math.min(r, g, b);
        let hue = 0, saturation = 0, lightness = (max + min) / 2;

        if (max !== min) {
            const delta = max - min;
            saturation = lightness > 0.5 ? delta / (2 - max - min) : delta / (max + min);
            switch (max) {
                case r: hue = ((g - b) / delta + (g < b ? 6 : 0)); break;
                case g: hue = ((b - r) / delta + 2); break;
                case b: hue = ((r - g) / delta + 4); break;
            }
            hue *= 60;
        }

        return {
            hue: Math.round(hue),
            saturation: Math.round(saturation * 100),
            lightness: Math.round(lightness * 100),
        };
    },
    
    evaluateScale() {
      const maxDifference = 1; 
      const minScale = 127;    
      const maxScale = 252;    
      const targetAverageDifference = this.mapValue(
        this.scale,
        maxScale,
        minScale,
        0, 
        maxDifference 
      );

      if (this.images.length < 2) {
        console.error("Not enough images to evaluate scale variation.");
        return 0;
      }

      let highVariationCount = 0;
      let lowVariationCount = 0;
      let totalPairs = 0;

      for (let i = 0; i < this.images.length; i++) {
        for (let j = i + 1; j < this.images.length; j++) {
          const imgA = this.images[i];
          const imgB = this.images[j];

          const originalRatio = imgA.originalWidth / imgB.originalWidth;

          const currentRatio = imgA.width / imgB.width;

          const relativeDifference = Math.abs(Math.log(currentRatio / originalRatio));

          if (relativeDifference >= targetAverageDifference) {
            highVariationCount++;
          } else {
            lowVariationCount++;
          }

          totalPairs++;
        }
      }

      const highVariationPercentage = highVariationCount / totalPairs;
      const lowVariationPercentage = lowVariationCount / totalPairs;
      
      if (this.scale >= 190) {
        if (highVariationPercentage === 1) {
          return 5; 
        } else if (highVariationPercentage >= 0.5) {
          return 3; 
        } else {
          return 0; 
        }
      } else {

        if (lowVariationPercentage === 1) {
          return 5; 
        } else if (lowVariationPercentage >= 0.5) {
          return 3; 
        } else {
          return 0; 
        }
      }
    },

    evaluateMotion() {
      let lowMotionCount = 0;
      let highMotionCount = 0;
      const rotationThreshold = Math.PI / 4;
      const totalImages = this.images.length;

      this.images.forEach((image) => {
        const deviation = Math.abs(image.rotation); 
        if (deviation <= rotationThreshold) {
          lowMotionCount++;
        } else {
          highMotionCount++;
        }
      });

      if (this.motion <= 63) {
        if (highMotionCount === totalImages) {
          return 5; 
        } else if (highMotionCount >= totalImages / 2) {
          return 3; 
        } else {
          return 0; 
        }
      } else {
        if (lowMotionCount === totalImages) {      
          return 5; 
        } else if (lowMotionCount >= totalImages / 2) {
          return 3; 
        } else {
          return 0; 
        }
      }
    },

    evaluateSpace() {
      const canvas = this.$refs.canvas;
      const quadrants = [
          { x1: 0, y1: 0, x2: canvas.width / 2, y2: canvas.height / 2 },         
          { x1: canvas.width / 2, y1: 0, x2: canvas.width, y2: canvas.height / 2 }, 
          { x1: 0, y1: canvas.height / 2, x2: canvas.width / 2, y2: canvas.height }, 
          { x1: canvas.width / 2, y1: canvas.height / 2, x2: canvas.width, y2: canvas.height }, 
      ];

      const calculateOccupiedArea = (quadrant) => {
          let occupiedArea = 0;

          for (const image of this.images) {
              const imageBounds = {
                  x1: image.x,
                  y1: image.y,
                  x2: image.x + image.width,
                  y2: image.y + image.height,
              };

              const intersectX = Math.max(0, Math.min(imageBounds.x2, quadrant.x2) - Math.max(imageBounds.x1, quadrant.x1));
              const intersectY = Math.max(0, Math.min(imageBounds.y2, quadrant.y2) - Math.max(imageBounds.y1, quadrant.y1));
              const intersectionArea = intersectX * intersectY;

              occupiedArea += intersectionArea;
          }

          const quadrantArea = (quadrant.x2 - quadrant.x1) * (quadrant.y2 - quadrant.y1);
          return occupiedArea / quadrantArea;
      };

      let fullyEmpty = 0;
      let partiallyEmpty = 0;

      for (const quadrant of quadrants) {
          const occupiedRatio = calculateOccupiedArea(quadrant);

          if (occupiedRatio === 0) {
              fullyEmpty++;
          } else if (occupiedRatio < 0.5) {
              partiallyEmpty++;
          } 
      }

      if (this.space <= 190) {
          if (fullyEmpty === 0){ 
            return 5; 
          }
          if (fullyEmpty < quadrants.length / 2) { 
            return 3; 
          }
          return 0; 
      } else {
          if (fullyEmpty >= 3 || (fullyEmpty === 2 && partiallyEmpty > 0)) { 
            return 5; 
          } 
          if (fullyEmpty >= 2 || (fullyEmpty === 1 && partiallyEmpty >= 2)) { 
            return 3; 
          }
          return 0;
      }
    },

    evaluateConcentration() {
      const canvas = this.$refs.canvas;
      if (!canvas) {
        console.error("Canvas element not found!");
        return 0;
      }

      const quadrants = {
        Q1: [],
        Q2: [],
        Q3: [],
        Q4: [],
      };

      const focusRadius = 50; 
      const clusters = [];

      this.images.forEach((image) => {
        const centerX = image.x + image.width / 2;
        const centerY = image.y + image.height / 2;

        let addedToCluster = false;
        for (const cluster of clusters) {
          const dx = cluster.centerX - centerX;
          const dy = cluster.centerY - centerY;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance <= focusRadius) {
            cluster.elements.push(image);
            cluster.centerX =
              (cluster.centerX * cluster.elements.length + centerX) /
              (cluster.elements.length + 1);
            cluster.centerY =
              (cluster.centerY * cluster.elements.length + centerY) /
              (cluster.elements.length + 1);
            addedToCluster = true;
            break;
          }
        }

        if (!addedToCluster) {
          clusters.push({
            centerX,
            centerY,
            elements: [image],
          });
        }
      });

      clusters.forEach((cluster) => {
        const { centerX, centerY } = cluster;
        if (centerX > canvas.width / 2 && centerY < canvas.height / 2) {
          quadrants.Q1.push(cluster);
        } else if (centerX < canvas.width / 2 && centerY < canvas.height / 2) {
          quadrants.Q2.push(cluster);
        } else if (centerX < canvas.width / 2 && centerY > canvas.height / 2) {
          quadrants.Q3.push(cluster);
        } else if (centerX > canvas.width / 2 && centerY > canvas.height / 2) {
          quadrants.Q4.push(cluster);
        }
      });

      const occupiedQuadrants = Object.values(quadrants).filter((q) => q.length > 0).length;

      let score = 0;
      if (this.concentration <= 63) {
        const oppositeQuadrants =
          (quadrants.Q1.length > 0 && quadrants.Q4.length > 0) ||
          (quadrants.Q2.length > 0 && quadrants.Q3.length > 0);

        const differentQuadrants = occupiedQuadrants > 1 && !oppositeQuadrants;

        if (oppositeQuadrants) {
          score += 5;
        } else if (differentQuadrants) {
          score += 3;
        }
      } else {
        if (occupiedQuadrants === 4) {
          score += 5;
        } else if (occupiedQuadrants >= 3) {
          score += 3;
        }
      }

      return score;
    },
    calculateQuadrantDistribution() {
      const quadrantsOccupied = new Set();

      this.images.forEach(image => {
          const xCenter = image.x + image.width / 2;
          const yCenter = image.y + image.height / 2;
          const quadrant = this.getQuadrant(xCenter, yCenter);
          quadrantsOccupied.add(quadrant);
      });

      return quadrantsOccupied.size;
    },
    getQuadrant(x, y) {
        const halfWidth = this.canvasWidth / 2;
        const halfHeight = this.canvasHeight / 2;

        if (x < halfWidth && y < halfHeight) return 1;
        if (x >= halfWidth && y < halfHeight) return 2;
        if (x < halfWidth && y >= halfHeight) return 3;
        return 4;
    },
    calculateEmptyQuadrants() {
        const quadrantsOccupied = new Set();

        this.images.forEach(image => {
            const xCenter = image.x + image.width / 2;
            const yCenter = image.y + image.height / 2;
            const quadrant = this.getQuadrant(xCenter, yCenter);
            quadrantsOccupied.add(quadrant);
        });

        return 4 - quadrantsOccupied.size;
    },

    evaluateTransparency() {      
      let NoneTransparencyCount = 0; 

      let highTransparencyCount = 0;
      let overlapCount = 0; 

      this.images.forEach((image, index) => {
        if (image.opacity >= 0.9){
          NoneTransparencyCount++;
        } else {
          highTransparencyCount++;
        }

        for (let i = index + 1; i < this.images.length; i++) {
          const otherImage = this.images[i];
          const isOverlapping =
            image.x < otherImage.x + otherImage.width &&
            image.x + image.width > otherImage.x &&
            image.y < otherImage.y + otherImage.height &&
            image.y + image.height > otherImage.y;

          if (isOverlapping) {
            overlapCount++;
            break; 
          }
        }
      });

      if (this.transparency >= 63) {
        if (NoneTransparencyCount === this.images.length) {
          return 5; 
        } else if (NoneTransparencyCount > this.images.length / 2) {
          return 3; 
        } else {
          return 0; 
        }
      }

      else {
        if (highTransparencyCount === this.images.length && overlapCount > 0) {
          return 5; 
        } else if (highTransparencyCount > this.images.length / 2 && overlapCount > 0) {
          return 3; 
        } else {
          return 0; 
        }
      }
    },

    evaluateAlignmentWithPrinciples() {
      const tempValue = this.mappingValue();
      const tempTransparency = this.mappingTransparency();
      const tempConcentration = this.mappingConcentration();
      const tempScale = this.mappingScale();
      const tempSpace = this.mappingSpace();
      const tempMotion = this.mappingMotion();

      const targetValues = {
        value: this.value,
        transparency: this.transparency,
        concentration: this.concentration,
        scale: this.scale,
        space: this.space,
        motion: this.motion
      };

      const differences = {
        value: Math.abs(tempValue - targetValues.value),
        transparency: Math.abs(tempTransparency - targetValues.transparency),
        concentration: Math.abs(tempConcentration - targetValues.concentration),
        scale: Math.abs(tempScale - targetValues.scale),
        space: Math.abs(tempSpace - targetValues.space),
        motion: Math.abs(tempMotion - targetValues.motion),
      };

      const alignedPrinciples = Object.values(differences).filter(diff => diff <= 0.3).length;
      const totalPrinciples = Object.keys(differences).length;
      if (alignedPrinciples === totalPrinciples) {
        return 5; 
      } else if (alignedPrinciples > totalPrinciples / 2) {
        return 3; 
      } else {
        return 0; 
      }
    },


    updateBackgroundCanvas() {
      this.previousStates = this.cloneCanvasState();
      if (this.hue === "360"){
        this.selectedColor = "#FFFFFF";
      } else if (this.hue === "0"){
        this.selectedColor = "#000000";
      } else {
        this.selectedColor = `hsl(${this.hue}, 60%, 50%)`
      }

      const ctx = this.$refs.canvas.getContext("2d");
      const canvas = this.$refs.canvas;
      if (canvas) {
        this.drawImages(ctx);
        canvas.style.backgroundColor = this.selectedColor;
        this.value = this.mappingValue();
        this.images.forEach((image) => {
          image.backgroundColor = this.selectedColor;
        });
        this.updatePoints();
        this.newState = this.cloneCanvasState(); 
      }
    },

    async finalizeColorChange() {      
      if (JSON.stringify(this.previousStates) !== JSON.stringify(this.newState)) {
        this.saveState();
        this.previousStates = this.newState;

        this.interacting = true;
        this.images = await this.generateAndSelectBestSolution();
        this.drawSuggestions();
        this.interacting = false;
      }
    },



    updateCanvasTransparency(index) {
      const ctx = this.$refs.canvas.getContext("2d");
      const canvas = this.$refs.canvas;

      if (canvas) {
        this.images[index].opacity = this.tranparencyLevel;

        let group = [];
        if (index === 0) {
          group = this.group3;
        } else if (index === 1) {
          group = this.group2;
        } else if (index === 4) {
          group = this.group4;
        } else if (index === 12) {
          group = this.group3_1;
        } else {
          group = this.group1.includes(this.images[index].id) ? this.group1 : this.group2;
        }

        group.forEach((cellId) => {
          if (cellId !== index) {
            this.images[cellId].opacity = this.tranparencyLevel;
          }
        });
        this.drawImages(ctx);

        this.transparency = this.mappingTransparency();
        this.updatePoints();
        this.newState = this.cloneCanvasState(); 
      }
    },

    async finalizeTransparencyChange() {      
      if (JSON.stringify(this.previousStates) !== JSON.stringify(this.newState)) {
        this.saveState();
        this.previousStates = this.cloneCanvasStateManual();

        this.interacting = true;
        this.images = await this.generateAndSelectBestSolution();
        this.drawSuggestions();
        this.interacting = false;
      }
    },

    toggleSlider() {
      this.showSlider = !this.showSlider; 
    },

    mappingScale() {
      let totalRelativeDifference = 0;
      let pairCount = 0;

      for (let i = 0; i < this.images.length; i++) {
        for (let j = i + 1; j < this.images.length; j++) {
          const imgA = this.images[i];
          const imgB = this.images[j];

          const originalRatio = (imgA.originalWidth/4) / (imgB.originalWidth/4);

          const currentRatio = imgA.width / imgB.width;

          const relativeDifference = Math.abs(Math.log(currentRatio / originalRatio));

          totalRelativeDifference += relativeDifference;
          pairCount++;
        }
      }

      if (pairCount === 0) {
        console.error("No image pairs found for comparison.");
        this.scale = 127; 
        return;
      }

      const averageRelativeDifference = totalRelativeDifference / pairCount;

      const maxDifference = 1; 
      const minScale = 127;    
      const maxScale = 252;    

      let mappedScale = this.mapValue(
        Math.min(maxDifference, averageRelativeDifference), 
        0, 
        maxDifference, 
        maxScale, 
        minScale 
      );

      if (isNaN(mappedScale)) {
        console.error("Mapped scale resulted in NaN. Defaulting to minScale.");
        mappedScale = minScale;
      } 

     return mappedScale;
    },

    mappingConcentration() {
      const minThreshold = 10; 
      const mappedMin = 127; 
      const mappedMax = 0;   

      const smoothingFactor = 0.03; 

      const elementCenters = [];
      const elementEffectiveAreas = [];

      for (const image of this.images) {
        const centerX = image.x + image.width / 2;
        const centerY = image.y + image.height / 2;
        const effectiveArea = this.calculateEffectiveArea(image, this.$refs.canvas);

        elementCenters.push({ x: centerX, y: centerY });
        elementEffectiveAreas.push(effectiveArea);
      }

      let closePairs = 0;
      let totalPairs = 0; 

      for (let i = 0; i < elementCenters.length; i++) {
        for (let j = i + 1; j < elementCenters.length; j++) {
          totalPairs++;
          const dx = elementCenters[i].x - elementCenters[j].x;
          const dy = elementCenters[i].y - elementCenters[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          const effectiveRadiusA = Math.sqrt(elementEffectiveAreas[i] / Math.PI);
          const effectiveRadiusB = Math.sqrt(elementEffectiveAreas[j] / Math.PI);
          
          const combinedRadius = effectiveRadiusA + effectiveRadiusB;

          const adjustedDistance = distance - combinedRadius;

          if (adjustedDistance < minThreshold) {
            closePairs++;
          }

        }
      }
      totalPairs = totalPairs/4;
      let proximityRatio = totalPairs > 0 ? closePairs / totalPairs : 0;
      proximityRatio = Math.max(0, Math.min(proximityRatio, 0.3));
      let mappedConcentration = this.mapValue(
        proximityRatio, 
        0, 
        0.3, 
        mappedMin,
        mappedMax
      );

      if (this.concentration !== undefined) {
        mappedConcentration = this.concentration + smoothingFactor * (mappedConcentration - this.concentration);
      } 
     return mappedConcentration;
    },

    mappingMotion() {
      const minMotion = 127;  
      const maxMotion = 0; 
      const maxRotation = Math.PI; 

      let totalDeviation = 0; 

      this.images.forEach((image) => {
          const rotation = Math.abs(image.rotation || 0) % (2 * Math.PI); 
          const deviation = Math.min(rotation, 2 * Math.PI - rotation);  
          totalDeviation += deviation / maxRotation; 
        });

      const averageDeviation = totalDeviation / this.images.length;

      let mappedMotion = this.mapValue(
        averageDeviation,
        0,
        1,
        minMotion,
        maxMotion
      );
      
      const smoothingFactor = 0.05;
      if (this.motion !== undefined) {
        mappedMotion = this.motion + smoothingFactor * (mappedMotion - this.motion);
      }

      return mappedMotion;
    },

    mappingValue() {
      const minValue = 0;   
      const maxValue = 127; 

      const mappedValue = this.mapValue(
        this.hue,
        0,
        360,
        minValue,
        maxValue
      );
      return mappedValue;
    },

    mappingTransparency() {
      const minTransparency = 0;   
      const maxTransparency = 127; 

      let transparencySum = 0;

      this.images.forEach((image) => {
        const opacity = Math.max(0, Math.min(image.opacity || 0, 1)); 
        transparencySum += opacity;
      });

      const averageTransparency = transparencySum / this.images.length;

      const mappedTransparency = this.mapValue(
        averageTransparency, 
        0.2, 
        1, 
        minTransparency, 
        maxTransparency 
      );

      return mappedTransparency;
    },

    mappingSpace() {
      const canvas = this.$refs.canvas;
      const canvasArea = canvas.width * canvas.height;

      let totalEffectivePixels = 0;

      for (const image of this.images) {
        const effectivePixels = this.calculateEffectiveArea(image, canvas);
        totalEffectivePixels += effectivePixels;
      }

      const occupationRatio = totalEffectivePixels / canvasArea;

      const mappedConcentration = this.mapValue(
        this.concentration,
        127,
        0,
        0,
        1
      );
      let emptySpaceScore = 1 - occupationRatio - (1 - mappedConcentration) * 0.3;
      if (emptySpaceScore < 0) {
        emptySpaceScore = 0;
      } else if(emptySpaceScore > 1) {
        emptySpaceScore = 1;
      }
      
      const minScale = 127;
      const maxScale = 252;
      let mappedSpace = this.mapValue(
        emptySpaceScore,
        0,
        0.75,
        minScale,
        maxScale
      );

      if (mappedSpace > maxScale){
        mappedSpace = maxScale;
      } else if (mappedSpace < minScale){
        mappedSpace = minScale;
      }
      return mappedSpace;
    },
    calculateEffectiveArea(image, mainCanvas) {
      const tempCanvas = document.createElement("canvas");
      tempCanvas.width = mainCanvas.width;
      tempCanvas.height = mainCanvas.height;
      const ctx = tempCanvas.getContext("2d");

      ctx.drawImage(image.image, image.x, image.y, image.width, image.height);

      const imageData = ctx.getImageData(
        image.x, image.y, image.width, image.height
      );

      let effectivePixels = 0;

      for (let i = 0; i < imageData.data.length; i += 4) {
        const alpha = imageData.data[i + 3];
        if (alpha > 0) {
          effectivePixels++;
        }
      }

      return effectivePixels;
    },

    mapValue(value, fromMin, fromMax, toMin, toMax) {
      return toMin + ((value - fromMin) * (toMax - toMin)) / (fromMax - fromMin);
    },

    toggleSelectionPrinciples(index) {
      this.principles[index].selected = !this.principles[index].selected;
    },

    async principlesContributions() {
      this.messagesToShow = [];
      const canvas = this.$refs.canvas;
      if (!canvas) {
        console.error("Canvas element not found!");
        return;
      }

      for (const principle of this.principles) {
        if (principle.selected) {
          switch (principle.name) {
            case "ELEMENTS":
              this.contributingElements();
              break;
            case "HUE":
              await this.contributingValue();
              break;
            case "TRANSPARENCY":
              await this.contributingTransparency();
              break;
            case "CONCENTRATION":
              await this.contributingConcentration();
              break;
            case "SCALE":
              await this.contributingScale();
              break;
            case "SPACE":
              await this.contributingSpace();
              break;
            case "MOTION":
              await this.contributingMotion();
              break;
          }
        }
      }

      this.updatePoints();
      const ctx = this.$refs.canvas.getContext("2d");
      this.drawImages(ctx);
      this.images = await this.generateAndSelectBestSolution();
      this.drawSuggestions();
    },

    contributingElements() {
      if (!this.images.length || !this.library_unit.length) {
        console.error("Images or library is empty!");
        return;
      }

      const randomImageIndex = Math.floor(Math.random() * this.images.length);
      const currentImageObj = this.images[randomImageIndex];
      const currentImageSrc = currentImageObj.src;

      const availableLibrary = this.library_unit.map((_, index) => index).filter(index => !this.solutions.includes(index));

      if (!availableLibrary.length) {
        console.warn("No available images to choose from!");
        return;
      }

      const newImageObj = availableLibrary[Math.floor(Math.random() * availableLibrary.length)];
      const newImageInfo = this.library_unit[newImageObj];
      const newBackgroundColor = newImageInfo[0].backgroundColor;

      const newImagePath = `/static/final_unit/sketch_${newImageObj}.png`;
      const newImage = new Image();
      newImage.src = newImagePath;

      newImage.onload = async () => {
        const originalWidth = newImage.width;
        const originalHeight = newImage.height;

  const aspectRatio = newImage.height / newImage.width;

  this.images = this.images.map((imageObj) => {
    const newWidth = imageObj.width;
    const newHeight = newWidth * aspectRatio;

    return {
      ...imageObj,
      image: newImage,
      src: newImagePath,
      width: newWidth,
      height: newHeight,
      originalWidth: originalWidth,
      originalHeight: originalHeight,
      backgroundColor: newBackgroundColor,
    };
  });


  this.solutions[0] = newImageObj;


  const createCanvasWithBackground = (imageSrc, backgroundColor) => {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    const canvasWidth = 100; 
    const canvasHeight = 100;
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    context.fillStyle = backgroundColor || "#ffffff";
    context.fillRect(0, 0, canvasWidth, canvasHeight);

    const image = new Image();
    image.src = imageSrc;

    return new Promise((resolve) => {
      image.onload = () => {
        const aspectRatio = image.height / image.width;
        const imgWidth = canvasWidth * 0.8; 
        const imgHeight = imgWidth * aspectRatio;

        const offsetX = (canvasWidth - imgWidth) / 2;
        const offsetY = (canvasHeight - imgHeight) / 2;

        context.drawImage(image, offsetX, offsetY, imgWidth, imgHeight);

        resolve(canvas.toDataURL("image/png"));
      };

      image.onerror = () => {
        console.error("Failed to load image for canvas:", imageSrc);
        resolve(null);
      };
    });
  };

  const oldImageCanvas = await createCanvasWithBackground(
    currentImageSrc,
    currentImageObj.backgroundColor
  );
  const newImageCanvas = await createCanvasWithBackground(
    newImagePath,
    newBackgroundColor
  );

  const message = {
    text: `
      <img style="padding: 2%; width: 30%;" src="${oldImageCanvas}" alt="Old Image">
      ▶
      <img style="padding: 2%; width: 30%;" src="${newImageCanvas}" alt="New Image">
    `,
  };

  this.messagesToShow.push(message);
  this.selectedColor = newBackgroundColor;
  this.images = await this.generateAndSelectBestSolution();
  const ctx = this.$refs.canvas.getContext("2d");
  this.drawImages(ctx);
  this.drawSuggestions();

  this.updatePoints();
};


  newImage.onerror = (error) => {
    console.error("Failed to load new image:", newImagePath, error);
  };
},

    async contributingValue() {
    this.message = "";
    let increment = 0;
    let actualValue = 127;
    const principleName = "HUE";

    if (!this.messageHistory) {
        this.messageHistory = [];
    }

    const conditions = [
        {
            condition: () => this.value >= 63 && this.transparency <= 63,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.max(0, this.value - increment);
                return "Increasing the hue allows you to create a visual play when you have a striking background.";

            }
        },
        {
            condition: () => this.value < 63 && this.transparency > 63,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.min(127, this.value + increment);
                return "Decreasing the hue highlights elements with little transparency.";

            }
        },
        {
            condition: () => this.value >= 63 && this.scale > 190,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.max(0, this.value - increment);
                return "Increasing the hue creates contrast and highlights elements that are far from the original scale.";

            }
        },
        {
            condition: () => this.value < 63 && this.scale <= 190,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.min(127, this.value + increment);
                return "Decreasing the hue removes the importance of the background and reinforces the closeness to the original scale of the elements.";

            }
        },
        {
            condition: () => this.value >= 63 && this.motion > 63,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.max(0, this.value - increment);
                return "Increasing the hue creates contrast in a composition without movement.";

            }
        },
        {
            condition: () => this.value < 63 && this.motion <= 63,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.min(127, this.value + increment);
                return "Decreasing the hue emphasises the elements, reinforcing the dynamism created by the movement.";

            }
        },
        {
            condition: () => this.value <= 63 && this.space < 190,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.max(0, this.value - increment);
                return "Increasing the hue allows you to emphasise the background in compositions with a lot of negative space.";

            }
        },
        {
            condition: () => this.value < 63 && this.space >= 190,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.min(127, this.value + increment);
                return "Reducing the hue makes it possible to create lightness in compositions with little negative space.";

            }
        },
        {
            condition: () => this.value >= 63 && this.concentration >= 63,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.max(0, this.value - increment);
                return "Increasing the hue allows you to highlight the elements that are scattered.";

            }
        },
        {
            condition: () => this.value < 63 && this.concentration < 63,
            action: () => {
                increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                this.value = Math.min(127, this.value + increment);
                return "Decreasing the hue allows the fund to be emphasised when the concentration is high.";

            }
        }
    ];

    const shuffledConditions = conditions.sort(() => Math.random() - 0.5);

    for (const { condition, action } of shuffledConditions) {
        if (condition()) {
            const potentialMessage = action();
            if (!this.messageHistory.includes(potentialMessage)) {
                this.message = potentialMessage;
                this.messagesToShow.push({
                    text: potentialMessage,
                    principle: principleName
                });
                break;
            }
        }
    }

    if (!this.message) {
        const repeatedCondition = shuffledConditions.find(({ condition }) => condition());
        if (repeatedCondition) {
            this.message = repeatedCondition.action();
            this.messagesToShow.push({
                    text: repeatedCondition.action(),
                    principle: principleName
                });
        }
    }

    this.images = await this.generateAndSelectBestSolution();
    },

    async contributingTransparency() {
      this.message = ""; 
      let increment = 0;
      let actualValue = 127;
      const principleName = "TRANSPARENCY";

      if (!this.messageHistory) {
        this.messageHistory = [];
      }

      const conditions = [
        {
          condition: () => this.value == 0 && this.transparency <= 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.min(127, this.transparency + increment);
            return "Reducing transparency highlights the elements on a neutral background.";
          }
        },
        {
          condition: () => this.value > 0 && this.transparency > 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.max(0, this.transparency - increment);
            return "Increasing transparency allows you to take advantage of the colour interaction between the background and the elements.";
          }
        },
        {
          condition: () => this.scale <= 190 && this.transparency <= 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.min(127, this.transparency + increment);
            return "Reducing transparency allows you to bring the elements even closer to their original format, bringing cohesion to the composition.";
          }
        },
        {
          condition: () => this.scale > 190 && this.transparency > 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.max(0, this.transparency - increment);
            return "Increasing transparency allows you to emphasise the distance between elements and their original format.";
          }
        },
        {
          condition: () => this.motion < 63 && this.transparency <= 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.min(127, this.transparency + increment);
            return "Reducing transparency emphasises the elements to reinforce movement.";
          }
        },
        {
          condition: () => this.motion >= 63 && this.transparency > 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.max(0, this.transparency - increment);
            return "Increasing transparency gives the composition more dynamism.";
          }
        },
        {
          condition: () => this.space < 190 && this.transparency <= 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.min(127, this.transparency + increment);
            return "Reducing transparency allows you to emphasise the elements, making them compete with the negative space.";
          }
        },
        {
          condition: () => this.space >= 190 && this.transparency > 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.max(0, this.transparency - increment);
            return "Increasing transparency allows you to create some dynamism by emphasising the background.";
          }
        },
        {
          condition: () => this.concentration >= 63 && this.transparency <= 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.min(127, this.transparency + increment);
            return "Reducing transparency reinforces the elements, preventing scattered areas from looking cluttered.";
          }
        },
        {
          condition: () => this.concentration < 63 && this.transparency > 63,
          action: () => {
            increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
            this.transparency = Math.max(0, this.transparency - increment);
            return "Increasing transparency creates depth and takes advantage of the overlap.";
          }
        }
      ];

      const shuffledConditions = conditions.sort(() => Math.random() - 0.5);

      for (const { condition, action } of shuffledConditions) {
        if (condition()) {
          const potentialMessage = action();
          if (!this.messageHistory.includes(potentialMessage)) {
            this.message = potentialMessage;
            this.messagesToShow.push({
                    text: potentialMessage,
                    principle: principleName
                });
            break;
          }
        }
      }

      if (!this.message) {
        const repeatedCondition = shuffledConditions.find(({ condition }) => condition());
        if (repeatedCondition) {
          this.message = repeatedCondition.action();
          this.messagesToShow.push({
                    text: repeatedCondition.action(),
                    principle: principleName
                });
        }
      }

      this.images = await this.generateAndSelectBestSolution();
    },

    async contributingMotion() {
        this.message = "";
        let increment = 0;
        let actualValue = 127;
        const principleName = "MOTION";

        if (!this.messageHistory) {
            this.messageHistory = [];
        }

        const conditions = [
            {
                condition: () => this.motion <= 63 && this.transparency > 63,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.min(127, this.motion + increment);
                    return "Decreasing the motion emphasises the elements with high transparency, reinforcing the movement.";
                }
            },
            {
                condition: () => this.motion > 63 && this.transparency <= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.max(0, this.motion - increment);
                    return "Increasing the movement gives the composition more dynamism.";
                }
            },
            {
                condition: () => this.motion <= 63 && this.value > 0,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.min(127, this.motion + increment);
                    return "Decreasing the motion can avoid visual conflicts, since the background is marked.";
                }
            },
            {
                condition: () => this.motion > 63 && this.value === 0,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.max(0, this.motion - increment);
                    return "Increasing the movement gives visual dynamism and offsets the neutrality of the background.";
                }
            },
            {
                condition: () => this.motion <= 63 && this.space < 190,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.min(127, this.motion + increment);
                    return "Decreasing the motion allows you to create a less confusing composition given the small amount of negative space.";
                }
            },
            {
                condition: () => this.motion > 63 && this.space >= 190,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.max(0, this.motion - increment);
                    return "Increasing motion introduces visual dynamics that complement the elevated negative space.";
                }
            },
            {
                condition: () => this.motion <= 63 && this.scale > 190,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.min(127, this.motion + increment);
                    return "Decreasing the motion allows the elements to be brought even closer to their original format, bringing cohesion to the composition.";
                }
            },
            {
                condition: () => this.motion > 63 && this.scale <= 190,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.max(0, this.motion - increment);
                    return "Increasing the movement makes it possible to emphasise the distance the elements have from the original format.";
                }
            },
            {
                condition: () => this.motion <= 63 && this.concentration >= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.min(127, this.motion + increment);
                    return "Decreasing the motion can help make the concentration of elements less visually confusing.";
                }
            },
            {
                condition: () => this.motion > 63 && this.concentration < 63,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.motion = Math.max(0, this.motion - increment);
                    return "Increasing movement helps to create dynamism in compositions with less concentration.";
                }
            }
        ];

        const shuffledConditions = conditions.sort(() => Math.random() - 0.5);

        for (const { condition, action } of shuffledConditions) {
            if (condition()) {
                const potentialMessage = action();
                if (!this.messageHistory.includes(potentialMessage)) {
                    this.message = potentialMessage;
                    this.messagesToShow.push({
                    text: potentialMessage,
                    principle: principleName
                });
                    break;
                }
            }
        }

        if (!this.message) {
            const repeatedCondition = shuffledConditions.find(({ condition }) => condition());
            if (repeatedCondition) {
                this.message = repeatedCondition.action();
                this.messagesToShow.push({
                    text: repeatedCondition.action(),
                    principle: principleName
                });
            }
        }

        this.messageHistory.push(this.message);
        if (this.messageHistory.length > 3) {
          this.messageHistory.shift();
        }

        this.images = await this.generateAndSelectBestSolution();
      },

    async contributingScale() {
        this.message = "";
        let increment = 0;
        let actualValue = 127;
        const principleName = "SCALE";

        if (!this.messageHistory) {
            this.messageHistory = [];
        }

        const conditions = [
            {
                condition: () => this.scale >= 190 && this.transparency > 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.scale = Math.max(127, this.scale - increment);
                    return "Decreasing the scale makes it possible to emphasise the distance between the elements and their original format, in a composition with a lot of transparency.";
                }
            },
            {
                condition: () => this.scale < 190 && this.transparency <= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;
                    this.scale = Math.min(254, this.scale + increment);
                    return "Increasing the scale brings the elements even closer to their original format, in a composition with little transparency.";
                }
            },
            {
                condition: () => this.scale >= 190 && this.value > 0,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;                     
                    this.scale = Math.max(127, this.scale - increment);
                    return "Decreasing the scale allows the elements to move away from their original format, in a composition where the background is important.";
                }
            },
            {
                condition: () => this.scale < 190 && this.value === 0,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;
                    this.scale = Math.min(254, this.scale + increment);
                    return "Increasing the scale allows you to bring the elements closer to their original format, emphasised against a background that is not very prominent.";
                }
            },
            {
                condition: () => this.scale >= 190 && this.motion >= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.scale = Math.max(127, this.scale - increment);
                    return "Decreasing the scale makes it possible to emphasise how far away the elements are from the original format.";
                }
            },
            {
                condition: () => this.scale < 190 && this.motion < 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;
                    this.scale = Math.min(254, this.scale + increment);
                    return "Increasing the scale brings the elements closer to their original format.";
                }
            },
            {
                condition: () => this.scale >= 190 && this.space < 190,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;                    
                    this.scale = Math.max(127, this.scale - increment);
                    return "Decreasing the scale brings the elements closer to their original format where the overall scale of the elements is low, giving the perception of cohesion.";
                }
            },
            {
                condition: () => this.scale < 190 && this.space >= 190,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;
                    this.scale = Math.min(254, this.scale + increment);
                    return "Increasing the scale allows you to move the elements away from their original format, in a composition where the overall scale of the elements is large and not close to the original.";
                }
            },
            {
                condition: () => this.scale >= 190 && this.concentration >= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;                    
                    this.scale = Math.max(127, this.scale - increment);
                    return "Decreasing the scale allows you to move the elements away from their original format, in a composition with a lot of concentration.";
                }
            },
            {
                condition: () => this.scale < 190 && this.concentration < 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;
                    this.scale = Math.min(254, this.scale + increment);
                    return "Increasing the scale allows the elements to be brought closer to their original format, emphasised in a composition with little concentration.";
                }
            }
        ];

        const shuffledConditions = conditions.sort(() => Math.random() - 0.5);

        for (const { condition, action } of shuffledConditions) {
            if (condition()) {
                const potentialMessage = action();
                if (!this.messageHistory.includes(potentialMessage)) {
                    this.message = potentialMessage;
                    this.messagesToShow.push({
                    text: potentialMessage,
                    principle: principleName
                });

                    break;
                }
            }
        }

        if (!this.message) {
            const repeatedCondition = shuffledConditions.find(({ condition }) => condition());
            if (repeatedCondition) {
                this.message = repeatedCondition.action();
                this.messagesToShow.push({
                    text: repeatedCondition.action(),
                    principle: principleName
                });

            }
        }

        this.images = await this.generateAndSelectBestSolution();
      },

    async contributingConcentration() {
        this.message = "";
        let increment = 0;
        let actualValue = 127;
        const principleName = "CONCENTRATION";

        if (!this.messageHistory) {
            this.messageHistory = [];
        }

        const conditions = [
            {
                condition: () => this.concentration <= 63 && this.transparency <= 63,
                action: () => {
                  increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                  this.concentration = Math.min(127, this.concentration + increment);
                  return "Decreasing the concentration avoids confusing overlaps with opaque elements.";
                }
            },
            {
                condition: () => this.concentration > 63 && this.transparency > 63,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.concentration = Math.max(0, this.concentration - increment);
                    return "Increasing concentration allows you to explore layers and visual overlays.";
                }
            },
            {
                condition: () => this.concentration <= 63 && this.value === 0,
                action: () => {
                  increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                  this.concentration = Math.min(127, this.concentration + increment);
                  return "Decreasing the concentration allows the elements to stand out, dispersing them.";
                }
            },
            {
                condition: () => this.concentration > 63 && this.value > 0,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.concentration = Math.max(0, this.concentration - increment);
                    return "Increasing concentration reinforces the visual impact on a striking background.";
                }
            },
            {
                condition: () => this.concentration <= 63 && this.motion >= 63,
                action: () => {
                  increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                  this.concentration = Math.min(127, this.concentration + increment);
                  return "Decreasing concentration can emphasise the movement of the elements, giving them space.";
                }
            },
            {
                condition: () => this.concentration > 63 && this.motion < 63,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.concentration = Math.max(0, this.concentration - increment);
                    return "Increasing concentration can give visual dynamism, as the elements have no movement.";
                }
            },
            {
                condition: () => this.concentration <= 63 && this.space <= 190,
                action: () => {
                  increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                  this.concentration = Math.min(127, this.concentration + increment);
                  return "Decreasing concentration allows you to take advantage of negative space and the elements.";
                }
            },
            {
                condition: () => this.concentration > 63 && this.space > 190,
                action: () => {
                    increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                    this.concentration = Math.max(0, this.concentration - increment);
                    return "Increasing the concentration makes it possible to increase the overall scale of the elements.";
                }
            },
            {
                condition: () => this.concentration <= 63 && this.scale > 190,
                action: () => {
                  increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                  this.concentration = Math.min(127, this.concentration + increment);
                  return "Decreasing the concentration allows you to bring the elements closer to their original format, emphasised in a composition with little concentration.";
                }
            },
            {
                condition: () => this.concentration > 63 && this.scale <= 190,
                action: () => {
                  increment = Math.floor(Math.random() * (actualValue - 0 + 1)) + 0;
                  this.concentration = Math.max(0, this.concentration - increment);
                  return "Increasing concentration allows you to move elements away from their original format by overlapping them.";
                }
            }
        ];

        const shuffledConditions = conditions.sort(() => Math.random() - 0.5);

        for (const { condition, action } of shuffledConditions) {
            if (condition()) {
                const potentialMessage = action();
                if (!this.messageHistory.includes(potentialMessage)) {
                    this.message = potentialMessage;
                    this.messagesToShow.push({
                    text: potentialMessage,
                    principle: principleName
                });

                    break;
                }
            }
        }

        if (!this.message) {
            const repeatedCondition = shuffledConditions.find(({ condition }) => condition());
            if (repeatedCondition) {
                this.message = repeatedCondition.action();
                this.messagesToShow.push({
                    text: repeatedCondition.action(),
                    principle: principleName
                });
            }
        }

        this.messageHistory.push(this.message);
        if (this.messageHistory.length > 3) {
          this.messageHistory.shift();
        }

        this.images = await this.generateAndSelectBestSolution();
      },

    async contributingSpace() {
        this.message = "";
        let increment = 0;
        let actualValue = 127;
        const principleName = "SPACE";

        if (!this.messageHistory) {
            this.messageHistory = [];
        }

        const conditions = [
            {
                condition: () => this.space >= 190 && this.transparency > 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.max(127, this.space - increment);
                    return "Decreasing the space can create visual dynamics due to the high transparency.";
                }
            },
            {
                condition: () => this.space < 190 && this.transparency <= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.min(254, this.space + increment);
                    return "Increasing the space emphasises the elements even more.";
                }
            },
            {
                condition: () => this.space >= 190 && this.value === 0,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.max(127, this.space - increment);
                    return "Decreasing the space compensates for the neutrality of the background, increasing the definition of the elements.";
                }
            },
            {
                condition: () => this.space < 190 && this.value > 0,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.min(254, this.space + increment);
                    return "Increasing the space makes it possible to create lightness in compositions with a highly emphasised background.";
                }
            },
            {
                condition: () => this.space >= 190 && this.scale <= 190,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.max(127, this.space - increment);
                    return "Decreasing the space makes it possible to increase the overall scale of the elements, emphasising the departure from their original format.";
                }
            },
            {
                condition: () => this.space < 190 && this.scale > 190,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.min(254, this.space + increment);
                    return "Increasing the space makes it possible to reduce the overall scale of the elements, emphasising their proximity to their original format.";
                }
            },
            {
                condition: () => this.space >= 190 && this.motion < 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.max(127, this.space - increment);
                    return "Decreasing the space can create more visual dynamics, since there is little movement in the elements.";
                }
            },
            {
                condition: () => this.space < 190 && this.motion >= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.min(254, this.space + increment);
                    return "Increasing the space introduces visual dynamics that complement the elevated movement.";
                }
            },
            {
                condition: () => this.space >= 190 && this.concentration < 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.max(127, this.space - increment);
                    return "Reducing the space makes it possible to take advantage of the negative space and the elements.";
                }
            },
            {
                condition: () => this.space < 190 && this.concentration >= 63,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.space = Math.min(254, this.space + increment);
                    return "Increasing the space takes advantage of the background and reduces the overall scale of the elements.";
                }
            }
        ];

        const shuffledConditions = conditions.sort(() => Math.random() - 0.5);

        for (const { condition, action } of shuffledConditions) {
            if (condition()) {
                const potentialMessage = action();
                if (!this.messageHistory.includes(potentialMessage)) {
                    this.message = potentialMessage;
                    this.messagesToShow.push({
                    text: potentialMessage,
                    principle: principleName
                });
                    break;
                }
            }
        }

        if (!this.message) {
            const repeatedCondition = shuffledConditions.find(({ condition }) => condition());
            if (repeatedCondition) {
                this.message = repeatedCondition.action();
                this.messagesToShow.push({
                    text: repeatedCondition.action(),
                    principle: principleName
                });
            }
        }

        this.images = await this.generateAndSelectBestSolution();

    },

    applyCanvasColor() {
      const canvas = this.$refs.canvas;
      if (canvas) {
        canvas.style.backgroundColor = this.selectedColor;
      }
    },

    updatePoints() {
      const angleBeta = 63.8;

      const adjustOnAxis = (x_real, angle) => {  
        const cos63_8 = Math.cos(angle * Math.PI / 180);
        const cosSquared = cos63_8 ** 2;

        const denominator = (1 / cosSquared) - 1;
        const aSquared = x_real ** 2 / denominator;
        return Math.sqrt(aSquared); 
      };

      const gettingTransparency = () => {
        let x = 0;
        if (this.value === 0) {
          x = 127;
        } else {
          x = 127 - this.value;
        }
        const sum = adjustOnAxis (x, angleBeta);
        let y = 0;
        if (this.value === 127) {
          y = this.transparency;
        } else {
          y = this.transparency + sum;
        }
        return y;
      };

      const gettingConcentration = () => {
        let x = 0;
        if (this.space === 127) {
          x = 127;
        } else { 
          x = this.space - 127; 
        }

        const sum = adjustOnAxis (x, angleBeta);
        let y = 0;
        if (this.space === 127) {
          y = this.concentration;
        } else {
          y = this.concentration + sum;
        }
        return y;
      };

      const gettingMotionScale = () => {
        let b = 0;
        if (this.scale === 127) {
          b = 127;
        } else {
          b = this.scale - 127;
        }
        const a = adjustOnAxis (b, angleBeta);

        let b1 = 0;
        if (this.motion === 127) {
          b1 = 127;
        } else {
          b1 = 127 - this.motion;
        }

        const a1 = adjustOnAxis (b1, angleBeta);
        let y = 0;
        if (this.scale === 127) {
          y = 127 + a1;
        } else {
          y = 127 + a + a1;
        }

        let x = this.scale - b1;
        return {x, y};
      };

      const point1 = {
        x: this.value, 
        y: gettingTransparency(), 
      };

      const motionScale = gettingMotionScale(); 
      const point2 = {
        x: motionScale.x, 
        y: motionScale.y,
      };

      const point3 = {
        x: this.space, 
        y: gettingConcentration(),
      };

      this.points = [point1, point2, point3];
    },

    setStructure(){
      const structureType = Math.random();
      let structureTypeIndex = 0;
      for (let i = 0; i < this.structureTypeThresholds.length; i++) {
        const [low, high] = this.structureTypeThresholds[i];
        if (low < structureType && structureType <= high) {
          structureTypeIndex = i + 1; 
          break;
        }
      }
      return structureTypeIndex;
    },

    drawImages(ctx) {
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); 
      this.images.forEach((imageObj, index) => {
        const { image, x, y, width, height, rotation, opacity } = imageObj;
        try {
          ctx.save();
          ctx.globalAlpha = opacity || 1; 
          ctx.translate(x + width / 2, y + height / 2);
          ctx.rotate(rotation || 0); 
          ctx.drawImage(image, -width / 2, -height / 2, width, height);
          ctx.restore();

          if (index === this.selectedItem && this.selectedItem !== null) {
            this.drawSelectionBox(ctx, x, y, width, height, rotation);
            if (isNaN(this.images[this.selectedItem].opacity)){
              this.tranparencyLevel = 0;
            } else {
              this.tranparencyLevel = this.images[this.selectedItem].opacity;
            }
          }
        } catch (err) {
          console.error("Error drawing image:", err, imageObj);
        }
      });
      ctx.canvas.style.backgroundColor = this.selectedColor;
      this.newState = this.cloneCanvasState();
    },

    drawSelectionBox(ctx, x, y, width, height, rotation) {
      ctx.save();
      ctx.translate(x + width / 2, y + height / 2);
      ctx.rotate(rotation);

      ctx.strokeStyle = "black";
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);

      ctx.strokeRect(-width / 2, -height / 2, width, height);

      const handleSize = 12;
      const handlePositions = [
        { x: -width / 2, y: -height / 2 }, 
        { x: width / 2, y: -height / 2 }, 
        { x: width / 2, y: height / 2 },  
        { x: -width / 2, y: height / 2 }, 
      ];

      ctx.fillStyle = "white";
      ctx.setLineDash([]);
      handlePositions.forEach((pos) => {
        ctx.beginPath();
        ctx.rect(pos.x - handleSize / 2, pos.y - handleSize / 2, handleSize, handleSize);
        ctx.fill();
        ctx.stroke();
      });

      const rotationHandleY = -height / 2;
      ctx.beginPath();
      ctx.arc(0, rotationHandleY, handleSize / 2, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    },

    startInteraction(event) {
    this.previousStates = this.cloneCanvasState();
    this.saveState();

    const { offsetX, offsetY } = event;
    const canvasWidth = this.$refs.canvas.width;
    const canvasHeight = this.$refs.canvas.height;

    const cellWidth = canvasWidth / 4; 
    const cellHeight = canvasHeight / 4; 

    const clickedCol = Math.floor(offsetX / cellWidth);
    const clickedRow = Math.floor(offsetY / cellHeight);

    if (this.selectedItem !== null) {
        const selectedImage = this.images[this.selectedItem];
        this.activeHandle = this.getHandleUnderCursor(event, selectedImage);

        if (this.activeHandle) {
          return; 
        }
      }
    
    const cellIndex = clickedRow * 4 + clickedCol;

    console.log(`Clicked cell: Row ${clickedRow}, Col ${clickedCol}, Index ${cellIndex}`);

    const clickedImageIndex = this.images.findIndex((imageObj) => {
      const { x, y, width, height, rotation } = imageObj;

      const centerX = x + width / 2;
        const centerY = y + height / 2;
        const cos = Math.cos(-rotation);
        const sin = Math.sin(-rotation);

        const localX = cos * (offsetX - centerX) - sin * (offsetY - centerY) + centerX;
        const localY = sin * (offsetX - centerX) + cos * (offsetY - centerY) + centerY;

        return (
          localX >= x &&
          localX <= x + width &&
          localY >= y &&
          localY <= y + height
        );
    });
    if (clickedImageIndex !== -1) {
        this.selectedItem = clickedImageIndex;
        const ctx = this.$refs.canvas.getContext("2d");
        this.drawImages(ctx); 
    } else {
        this.selectedItem = null;
        this.activeHandle = null;
        const ctx = this.$refs.canvas.getContext("2d");
        this.drawImages(ctx); 
    }

    if (this.selectedItem !== null) {
        const selectedImage = this.images[this.selectedItem];
        this.dragging = {
            offsetX: offsetX - selectedImage.x,
            offsetY: offsetY - selectedImage.y,
        };
    } else {
        this.dragging = null;
    }
},

    interact(event) {
      if (this.selectedItem !== null) {
          const { offsetX, offsetY } = event;
          const imageObj = this.images[this.selectedItem];
          let deltaX = 0, deltaY = 0, deltaRotation = 0, deltaWidth = 0, deltaHeight = 0;

          const initialState = {
            x: imageObj.x,
            y: imageObj.y,
            width: imageObj.width,
            height: imageObj.height,
            rotation: imageObj.rotation
          };

          let group = [];
          if (this.selectedItem == 0) {
            group = this.group3;
          } else if (this.selectedItem == 1) {
            group = this.group2;
          }
          else if (this.selectedItem == 4) {
            group = this.group4;
          } else if (this.selectedItem === 12) {
            group = this.group3_1;
          } else {
            group = this.group1.includes(imageObj.id) ? this.group1 : this.group2;
          }
          
          const canvasWidth = this.$refs.canvas.width;
          const canvasHeight = this.$refs.canvas.height;
          const cellWidth = canvasWidth / 4; 
          const cellHeight = canvasHeight / 4; 

          const cellRow = Math.floor(imageObj.id / 4); 
          const cellCol = imageObj.id % 4; 
          const cellStartX = cellCol * cellWidth; 
          const cellStartY = cellRow * cellHeight; 

          if (this.activeHandle) {
            if (this.activeHandle.type === "resize") {
              const centerX = imageObj.x + imageObj.width / 2;
              const centerY = imageObj.y + imageObj.height / 2;

              const dx = offsetX - centerX;
              const dy = offsetY - centerY;
              const newDistance = Math.sqrt(dx * dx + dy * dy);

              const initialDistance = Math.sqrt((imageObj.width / 2) ** 2 + (imageObj.height / 2) ** 2);
              const scaleFactor = newDistance / initialDistance;

              const minSize = 20; 
              const newWidth = Math.max(minSize, imageObj.width * scaleFactor);
              const newHeight = (imageObj.height / imageObj.width) * newWidth;

              imageObj.width = newWidth;
              imageObj.height = newHeight;

              deltaWidth = imageObj.width;
              deltaHeight = imageObj.width;

              this.scale = this.mappingScale();
              this.space = this.mappingSpace();
              this.updatePoints();
            } else if (this.activeHandle.type === "rotate") {
              const centerX = imageObj.x + imageObj.width / 2;
              const centerY = imageObj.y + imageObj.height / 2;
              imageObj.rotation = Math.atan2(offsetY - centerY, offsetX - centerX);
              deltaRotation = imageObj.rotation - initialState.rotation; 

              this.motion = this.mappingMotion();
              this.updatePoints();
            }
          } else if (this.dragging) {
            const newX = offsetX - this.dragging.offsetX;
            const newY = offsetY - this.dragging.offsetY;

            const maxX = cellStartX + cellWidth;
            const maxY = cellStartY + cellHeight;
            const minX = cellStartX - cellWidth;
            const minY = cellStartY - cellHeight;

            imageObj.x = Math.min(Math.max(newX, minX), maxX);
            imageObj.y = Math.min(Math.max(newY, minY), maxY);

            deltaX = newX - initialState.x;
            deltaY = newY - initialState.y;
            
            this.concentration = this.mappingConcentration();
            this.space = this.mappingSpace();
            this.updatePoints();
          }
        group.forEach((cellId) => {
          if (cellId !== this.selectedItem){
            const targetImage = this.images[cellId];

            const cellRow = Math.floor(cellId / 4);
            const cellCol = cellId % 4;
            const cellStartX = cellCol * cellWidth;
            const cellStartY = cellRow * cellHeight;

            if (this.activeHandle) {
              if (this.activeHandle.type === "resize") {
                targetImage.width = deltaWidth;
                targetImage.height = deltaHeight;
              } else if (this.activeHandle.type === "rotate") {
                targetImage.rotation += deltaRotation;
              }
            } else if (this.dragging) {
              const newX = targetImage.x + deltaX;
              const newY = targetImage.y + deltaY;
              
              const maxX = cellStartX + cellWidth;
              const maxY = cellStartY + cellHeight;
              const minX = cellStartX - cellWidth;
              const minY = cellStartY - cellHeight;

              targetImage.x = Math.min(Math.max(newX, minX), maxX);
              targetImage.y = Math.min(Math.max(newY, minY), maxY);
            }
          }
        });
        
        const ctx = this.$refs.canvas.getContext("2d");
        this.drawImages(ctx);
      }
    },


    async stopInteraction() {
      this.dragging = null;
      this.activeHandle = null;

      this.newState = this.cloneCanvasState();

      if (JSON.stringify(this.previousStates) !== JSON.stringify(this.newState) && this.firstLoad === false) {
          this.interacting = true;
          this.images = await this.generateAndSelectBestSolution();
          this.drawSuggestions();
        }


      this.interacting = false;
    },

    getHandleUnderCursor(event, imageObj) {
      const { offsetX, offsetY } = event;
      const { x, y, width, height, rotation } = imageObj;

      const centerX = x + width / 2;
      const centerY = y + height / 2;

      const cos = Math.cos(-rotation);
      const sin = Math.sin(-rotation);

      const localX = cos * (offsetX - centerX) - sin * (offsetY - centerY);
      const localY = sin * (offsetX - centerX) + cos * (offsetY - centerY);

      const handleSize = 8;

      const handlePositions = [
        { x: -width / 2, y: -height / 2 }, 
        { x: width / 2, y: -height / 2 }, 
        { x: width / 2, y: height / 2 },  
        { x: -width / 2, y: height / 2 }, 
      ];

      for (let i = 0; i < handlePositions.length; i++) {
        const handle = handlePositions[i];
        const handleX = handle.x - handleSize / 2;
        const handleY = handle.y - handleSize / 2;

        if (
          localX >= handleX &&
          localX <= handleX + handleSize &&
          localY >= handleY &&
          localY <= handleY + handleSize
        ) {
          return { type: "resize", index: i }; 
        }
      }

      const rotationHandleY = -height / 2;
      const rotationHandleX = 0;

      if (
        localX >= rotationHandleX - handleSize / 2 &&
        localX <= rotationHandleX + handleSize / 2 &&
        localY >= rotationHandleY - handleSize / 2 &&
        localY <= rotationHandleY + handleSize / 2
      ) {
        return { type: "rotate" };
      }

      return null; 
    },

    drawSuggestions() {
      this.suggestions.forEach((suggestion, index) => {
        const canvas = this.$refs[`suggestionCanvas${index}`][0];
        if (!canvas) {
          console.warn(`Canvas para a sugestão ${index} not found!`);
          return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          console.error(`Falha ao obter o contexto 2D para a sugestão ${index}`);
          return;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        suggestion.forEach((imageObj) => {
          const { image, x, y, width, height, rotation, opacity } = imageObj;

          if (!image) {
            console.warn("Imagem inválida numa sugestão:", imageObj);
            return; 
          }

            ctx.save();
            ctx.globalAlpha = opacity || 1; 
            ctx.translate(x + width / 2, y + height / 2);
            ctx.rotate(rotation || 0);
            ctx.drawImage(image, -width / 2, -height / 2, width, height);
            ctx.restore();
            
        });
        ctx.canvas.style.backgroundColor = this.selectedColor;
      });
    },
    
    acceptSuggestion(index) {
      const selectedSuggestion = this.suggestions[index];

      this.images = selectedSuggestion; 

      this.updatePoints();
      const ctx = this.$refs.canvas.getContext("2d");
      this.drawImages(ctx);
    },

    startDrag(index) {
      this.draggingPointIndex = index;
      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },
    onDrag(event) {
      if (this.draggingPointIndex !== null) {
        const svg = document.querySelector("svg");
        const point = svg.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;

        const svgPoint = point.matrixTransform(svg.getScreenCTM().inverse());

        this.points[this.draggingPointIndex] = {
          x: Math.max(0, Math.min(254, svgPoint.x)), 
          y: Math.max(0, Math.min(254, svgPoint.y)) 
        };
      }
    },
    stopDrag() {
      this.draggingPointIndex = null;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
    },

  
    isSelected(imageSrc) {
      const imageIndex = this.library_unit.findIndex(item => item === imageSrc);
      return this.solutions.includes(imageIndex);
    },

    async toggleSelection(imageSrc) {
        const imageIndex = this.library_unit.findIndex(item => item === imageSrc);        
        if (!this.solutions) {
            console.warn("solutions is undefined");
            return;
        }

        const canvas = this.$refs.canvas;
        const ctx = canvas.getContext("2d");

        this.solutions = [imageIndex];
        this.images = [];

        const imagePaths = [`/static/final_unit/sketch_${imageIndex}.png`];

        const imagePromises = imagePaths.map((path,imgIndex) => {
          return new Promise((resolve, reject) => {
                const img = new Image();
                img.src = `${path}?t=${new Date().getTime()}`;

                img.onload = () => {
                  const canvasWidth = this.$refs.canvas.width;
                  const canvasHeight = this.$refs.canvas.height;

                  const cellWidth = canvasWidth / 4; 
                  const cellHeight = canvasHeight / 4; 

                  const group = this.library_unit[this.solutions[imgIndex]] || [];
                  const backgroundColor = group[0]?.backgroundColor || '#ffffff'; 
                  this.selectedColor = backgroundColor;
                  this.selectedColor = backgroundColor;
                  if (this.selectedColor == "#FFFFFF" ) {
                    this.hue = 360;
                    this.selectedColor == "#FFFFFF";
                  }
                  else if (this.selectedColor == "#000000") {
                    this.hue = 0 ;
                    this.selectedColor == "#000000"
                  } else {
                    const match = backgroundColor.match(/hsl\(([\d.]+),/);
                    this.hue = parseFloat(match[1]);
                  }
                  
                  this.value = this.mappingValue();
                  this.updatePoints();
                  this.newState = this.cloneCanvasState();
                  for (let gridRow = 0; gridRow < 4; gridRow++) {
                    for (let gridCol = 0; gridCol < 4; gridCol++) {
                      this.images.push({
                        id: gridRow * 4 + gridCol + imgIndex * 16, 
                        image: img,
                        src: img.src,
                        x: gridCol * cellWidth,
                        y: gridRow * cellHeight,
                        width: cellWidth,
                        height: cellHeight,
                        originalWidth: img.width,
                        originalHeight: img.height,
                        rotation: 0,
                        opacity: 1,
                        backgroundColor: backgroundColor,
                      });
                    }
                  }
                  resolve();
                };
                img.onerror = (error) => reject(error);
            });
        });
        try {
            await Promise.all(imagePromises);
        } catch (error) {
            console.error("Error loading images:", error);
        }
      
        this.newState = this.cloneCanvasState();
        this.interacting = true;


        this.images = await this.generateAndSelectBestSolution();
        this.drawImages(ctx);

        this.drawSuggestions();

        this.updatePoints();

        this.interacting = false;
    },

    showInfo(index) {
      const libraryName = this.library_names[index];
      const match = libraryName.match(/\/(\d+)_/);
      const id = match[1]; 
      const libraryIndex = this.library[index]
      const match_index = libraryIndex.match(/\/(\d+)\.png/); 
      const number_library = match_index[1]; 
    
      if (id === number_library){
        const name = libraryName.split('/').pop();
        const match_name = name.match(/_(.+)$/);
        const match_name1 = match_name[1];
        const imageName = match_name1.split('.').slice(0, -1).join('.'); 
        const decomposedData = this.decomposed_info.find((info) => {
          const decomposedImageName = info.id_imagem.split('/').pop();
          return decomposedImageName === imageName;
        });
        if (decomposedData) {
          this.hoveredInfo = {
            imagePath: decomposedData.id_imagem,
            keywords: Array.isArray(decomposedData.palavras_chave)
              ? decomposedData.palavras_chave.join(', ')
              : decomposedData.palavras_chave,
            relation: decomposedData.relation,
            probabilities: Array.isArray(decomposedData.prob)
              ? decomposedData.prob.join(', ')
              : decomposedData.prob,
          };
        } else {
          this.hoveredInfo = null; 
        }
      }

      
    },
    hideInfo() {
      this.hoveredInfo = null;
    },
    

    cleanCanvas() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext("2d");

      if (ctx) {
          ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      }

      this.images = []; 
      this.solutions.src = [];
      this.selectedItem = null; 
      this.previousStates = [];
      this.newState = [];

      this.selectedColor = "FFFFFF";
      this.hue = "360";
      this.value = 127;
      this.motion = 127;
      this.scale = 100;
      this.concentration = 127;
      this.space = 127;
      this.transparency = 127;
      this.suggestions = [];

      this.updatePoints();
      this.updateBackgroundCanvas();
    },

    undo() {
      this.redoStack.push(this.newState);
      if (this.previousState ==="undefined"){
        this.previousState = this.cloneCanvasState();

      } else{
        this.previousState = this.undoStack[this.undoStack.length - this.counterUndo];

      }
      this.images = this.previousState;
      
      this.images.forEach((image) => {
          this.selectedColor = image.backgroundColor;
        });

      const ctx = this.$refs.canvas.getContext("2d");
      this.drawImages(ctx);
      this.counterRedo+=1;
      this.counterUndo = 0;
      this.undoStack = [];
    },

    redo() {      
      this.newState = this.redoStack[this.redoStack.length - this.counterRedo];
      this.images = this.newState;
      this.images.forEach((image) => {
          this.selectedColor = image.backgroundColor;
        });
      const ctx = this.$refs.canvas.getContext("2d");
      this.drawImages(ctx);
      
      this.redoStack = [];
      this.counterRedo = 0;
    },

    saveState() {
      if (this.previousStates === "undefined"){
        this.previousStates = this.cloneCanvasState();
      } else {
        this.undoStack.push(this.previousStates);
      }
      
      this.redoStack = [];
      this.counterUndo+=1;
      this.counterRedo = 0;
    },

    async expand() {
      const canvas = this.$refs.canvas;
      const patternName = "my_custom_pattern";

      const path = await this.expandPattern(canvas, patternName);

      if (path) {
        window.open(path, "_blank");
      }
    },

    async expandPattern(canvas, patternName) {
      const canvasData = canvas.toDataURL("image/png");
      const image_expand = this.cloneCanvasStateSource();

      axios
        .post("http://127.0.0.1:5000/api/expand-pattern", {
            canvasData: canvasData,
            patternName: patternName,
            imagesInfo: image_expand,
        })
        .then((response) => {
          if (response.data.success) {
            const patternPath = response.data.patternPath;
            this.expandPath = patternPath;
            this.showPopup = true;
          } else {
            console.error("Error: ", response.data.message);
          }
        })
        .catch((error) => {
          console.error("Error API:", error);
        });
        
    }, 
    closePopup() {
      this.showPopup = false; 
      this.patternPath = "";  
    },
    cloneCanvasStateSource() {
      if (!Array.isArray(this.images)) {
        console.error("Error: 'images' is not an array or is undefined.");
        return [];
      }

      return this.images.map(imageObj => ({
        ...imageObj,
        image: imageObj.image.src, 
      }));
    },  

    export_sketch() {
      const saving = this.cloneCanvasState();
      this.sketches.push(saving);
      this.$nextTick(() => {
        this.drawSaved();
        this.saveCanvasToFile();
      });
    },


    drawSaved() {
      let color = "";
      this.sketches.forEach((sketch, index) => {
        const canvas = this.$refs[`sketchesCanvas${index}`][0];
        if (!canvas) {
          console.warn(`Canvas for suggestion ${index} not found!`);
          return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          console.error(`Falha ao obter o contexto 2D para a sugestão ${index}`);
          return;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        sketch.forEach((imageObj) => {
          const { image, x, y, width, height, rotation, opacity, backgroundColor } = imageObj;
          color = backgroundColor
          if (!image) {
            console.warn("Invalid image in suggestion:", imageObj);
            return; 
          }

          ctx.save();
          ctx.globalAlpha = opacity || 1; 
          ctx.translate(x + width / 2, y + height / 2);
          ctx.rotate(rotation || 0);
          ctx.drawImage(image, -width / 2, -height / 2, width, height);
          ctx.restore();
        });

        ctx.canvas.style.backgroundColor = color || "#fff"; 
      });


    },
    saveCanvasToFile() {
      this.sketches.forEach((sketch, index) => {
        const canvas = this.$refs[`sketchesCanvas${index}`][0];
        if (!canvas) {
          console.warn(`Canvas for suggestion ${index} not found!`);
          return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          console.error(`Falha ao obter o contexto 2D para a sugestão ${index}`);
          return;
        }

        const color = sketch[0]?.backgroundColor || "#ffffff";
        ctx.save();
        ctx.fillStyle = color;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.restore();

        sketch.forEach((imageObj) => {
          const { image, x, y, width, height, rotation, opacity } = imageObj;
          if (!image) return;
          ctx.save();
          ctx.globalAlpha = opacity || 1;
          ctx.translate(x + width / 2, y + height / 2);
          ctx.rotate(rotation || 0);
          ctx.drawImage(image, -width / 2, -height / 2, width, height);
          ctx.restore();
        });

        const dataUrl = canvas.toDataURL("image/png");
        const fileName = `sketch_${index}.png`;

        fetch("/api/save_final_pattern", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            imageData: dataUrl,
            fileName: fileName,
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (!data.success) {
              console.error("Error on upload:", data.message);
            }
          })
          .catch((err) => console.error("Failed to send image:", err));

        const link = document.createElement("a");
        link.href = dataUrl;
        link.download = fileName;
        link.click();
      });
    },

    drawLibrary() {
      this.$nextTick(() => {
        const canvasRefs = this.$refs.libraryCanvas;
        if (!canvasRefs || canvasRefs.length === 0) {
          console.warn("No canvases found!");
          return;
        }

        this.library_unit.forEach((unit, index) => {
          const canvas = canvasRefs[index];

          if (!canvas) {
            console.warn(`Canvas for library ${index} not found!`);
            return;
          }

          const ctx = canvas.getContext("2d");

          if (!ctx) {
            console.error(`Failed to get 2D context for library ${index}`);
            return;
          }

          ctx.clearRect(0, 0, canvas.width, canvas.height);

          let color = "#fff"; 

          unit.forEach((imageObj) => {
            const { src, x, y, width, height, rotation, opacity, backgroundColor } = imageObj;

            if (!src) {
              console.warn("Invalid image in unit:", imageObj);
              return;
            }

            const img = new Image();
            img.src = `${src}`;

            img.onload = () => {
              ctx.save();
              ctx.globalAlpha = opacity || 1; 
              ctx.translate(x + width / 2, y + height / 2);
              ctx.rotate((rotation || 0)); 
              ctx.drawImage(img, -width / 2, -height / 2, width, height);
              ctx.restore();
            };

            img.onerror = () => {
              console.error(`Failed to load image: ${img.src}`);
            };

            if (backgroundColor) {
              color = backgroundColor;
            }
          });

          ctx.canvas.style.backgroundColor = color;
        });
      });
    },
  },
};
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.popup-content {
  background: #f8f2e6;
padding: 20px;
border-radius: 8px;
text-align: center;
}

.popup-content img {
  max-width: 50%;
  height: auto;
  margin-bottom: 20px;
}

.footerpattern{
  align-items: start;
  justify-content: space-between;
  display: flex;
  width: 95%;
  margin-bottom: 1.5rem;
  flex-direction: column;
}
.nav {
  opacity: 0.6;
  font-size: 9px;
}
.nav.active {
  opacity: 1;
}
.navigation-names {
  margin-top: 0.3rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 30%;
}
.popup-content button {
  background: none;
  color: #000;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 44px;
  position: absolute;
  top: 1.5rem;
  right: 5rem;
}

.unit-development {
  font-family: Arial, sans-serif;
  color: #4a2e2e;
  background-color: #f8f2e6;
  padding: 20px;
}

.title {
  text-align: left;
  font-size: 2rem;
  margin-bottom: 20px;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
}

.library,
.principles {
  padding: 0 5%;
}
.sketches {
  padding: 1rem 0;
  border-top: 2px solid #A67E66;
}
.suggestions {
 padding: 1rem 5%;
 border-top: 2px solid #A67E66;
}

/* Library Items */
.library-item {
  width: 40%;
  margin-right: 22%;
  padding: 2%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: none;
  border: none;
  cursor: pointer;
  gap: 10px;
}

.library-item img {
  width: 50px;
  margin-right: 10px;
}

.library-item:hover {
  background-color: #f2e8d6;
  border-radius: 5px;
}

.info-button {
  background: none;
  border: none;
  color: black;
  padding: 5px 10px;
  font-size: 0.8rem;
  cursor: pointer;
}

.library-item.selected {
  border: 1px solid rgb(0, 0, 0); 
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(229, 229, 234, 0.5);
}
.info-popup{
  position: absolute;
  top: 7rem;
  left: 25rem;
  width: 20%;
  background-color:#efe3d1;
  font-size: 13px;
  border-radius: 2px;
  display: flex;
  flex-direction: column;
}

.info-popup img{
  width: 100%;
  margin:auto;
  padding: 1rem;
}
.description{
  margin: auto;
  width: 100%;
  padding: 0 1rem 1rem 1rem;
}


/* Canvas */
.opacity-slider {
  position: absolute;
  top: 6%;
  left: 44%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  font-size: 11px;
}

.color-slider{
  width: 100%;
}

.slider-container{
  position: absolute;
  top: 10%;
  left: 28%;
  background-color: #efe3d1;
  width: 10%;
  height: 2%;
  border-radius: 7px;
}

.first-displayarea{
  display: grid;
  grid-template-columns: 2fr 6fr;
  grid-template-rows: auto auto;
  width: 95%;
}

.bottom-icons{
  display: flex;
  flex-direction: column;
  width: 92%;
  align-items: end;
  height: auto;
  gap: 2%
}

.bottom-icons > button{
  background: none;
  border: none;
}
.bottom-icons > button > img {
  width: 100%;
}

.canvas {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  height: width;
  width: 345px;
  height: 345px;
}

.main-sketch {
  width: auto;
  max-height: 90%;
}

.placeholder {
  color: #a49c8e;
  font-size: 1.2rem;
  text-align: center;
}
.graph-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px;
}

.draggable {
  cursor: pointer;
}

/* Sketches */
.sketch-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  max-height: 9rem;
  overflow-y: auto;
  padding-right: 1rem;
  margin-top: 1.5rem;
}

.sketch-grid[data-v-3e1ff366]::-webkit-scrollbar-thumb {
background-color: #A67E66;
border-radius: 20px;
border: none;
}
.sketch-grid::-webkit-scrollbar {
  width: 0.5rem;         
}
.sketch-grid::-webkit-scrollbar-track{
  background: #efe3d1;
}
.suggestion-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.sketch-thumbnail,
.suggestion-thumbnail {
  width: 100%;
  height: auto;
}

.expand {
  width: 13%;
}
.clean,
.undo,
.redo {
  width: 11%;
}
.export {
  width: 12%;
}
.color{
  width: 21%;
  display: flex;
}

.color-circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #ccc;
  display: inline-block;
  vertical-align: middle;
}

.dropdown-arrow {
  font-size: 11px;
  margin-right: 3px;
  margin-top: 3px;
  color: black;
}




.buttons-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(4rem, 1fr));
  gap: 1rem;
  width: 100%;
  margin-bottom: 0.7rem;
}
.principle-button {
  background: none;
  border: 2px solid #A67E66;
  height: 2rem;
  width: 6.7rem;
  font-size: 11px;
}
.principles-caption{
  font-size: 10px;
  margin: 0.7rem 0;
}
.explainable-container{
  height: 1em;
}
.justification-message{
  height: 10rem;
  font-size: 13px;
  max-height: 10rem; 
  overflow-y: auto;
}
.justification-message::-webkit-scrollbar {
  width: 0.5rem;              
}
.justification-message::-webkit-scrollbar-track{
  background: #efe3d1;
}
.justification-message::-webkit-scrollbar-thumb {
  background-color: #A67E66;
  border-radius: 20px;
  border: none;
}

.message-item{
  margin-bottom: 0.7rem;
}
.change-section{
  display: flex;
  width: 103%;
  justify-content: end;
}
.check-mark{
  background: none;
  border: none;
  cursor: pointer;
  color: black;
}
.changeImage{
  width: 10%;
}
.change-section .check-mark.disabled {
  opacity: 0.5; 
  cursor: not-allowed; 
}

/* Suggestions */
.develop-button {
  margin-top: 10px;
  background-color: #d3a38f;
  border: none;
  color: white;
  padding: 10px;
  width: 100%;
  font-size: 0.9rem;
  cursor: pointer;
}



</style>