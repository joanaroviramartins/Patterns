<template>
  <div class="section" id="gallery">
    <!-- Título -->
    <div class="gallery-header">
        <h1 class="gallery-title">UNIT</h1>
        <!-- Searched Term -->
        <div class="search-container" v-if="searchedTerm">
            <p class="bold searchTermTitle">Searched Word(s)</p>
            <div class="searchTerm" id="searchTermGallery">{{ searchedTerm }}</div>
        </div>

        <!-- Semantic Words -->
        <div class="relatedWordsContainer" v-if="semanticSearch && semanticSearch.length">
          <p class="bold relatedWordsTitle">Related Words List</p>
          <div class="relatedWords" id="relatedWordsGallery">{{ semanticSearch.join(", ") }}</div>
        </div>
    </div>
    <div class="warning"></div>
    <div class="container-unit">
      <aside class="left-menu">
        <h2>LIBRARY</h2>
        <div class ="images-container-left">
          <div class="images-container" id="elements-images">
            <div v-if="library && library.length" class="object">
              <div
                v-for="(item, index) in library"
                :key="index"
                class="library-item"
                :class="{ selected: isSelected(item) }"
                @click="toggleSelection(item)"
              >
                <img :src="item" alt="element" />
                <button 
                  class="info-button" 
                  @mouseover="showInfo(index)" 
                  @mouseleave="hideInfo"
                >
                  INFO+
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="hoveredInfo" class="info-popup">
          <img :src="hoveredInfo.imagePath" alt="Info Image" />
          <div class="description">
            <p><strong>Searched Term:</strong> {{ hoveredInfo.keywords }}</p>
            <p><strong>Relation:</strong> {{ hoveredInfo.relation }}</p>
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
            @mousedown="previousStates = cloneCanvasState()"
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

          <circle
            v-for="(point, index) in points"
            :key="index"
            class="draggable"
            :cx="point.x"
            :cy="point.y"
            r="4"
            fill="#000"
            @mousedown="startDrag(index)"
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
    <div class="footer">
      <div class="progress">
        <div class="navigationGeneral">
          <span class="nav-circle"></span>
          <span class="nav-line"></span>
          <span class="nav-circle"></span>
          <span class="nav-line"></span>
          <span class="nav-circle active"></span>
          <span class="nav-line"></span>
          <span class="nav-circle"></span>
        </div>
        <div class="navigation-namesGeneral">
            <span class="nav">GALLERY</span>
            <span class="nav">SELECTED GALLERY</span>
            <span class="nav active">UNIT DEVELOPMENT</span>
            <span class="nav">PATTERN</span>
          </div>
      </div>
        <div class="div-arrow">
          <span id="submit">DEVELOP YOUR UNIT TO USE IN THE PATTERN</span>
          <div class="nav-arrow" @click="pattern">▶</div>
        </div>
    </div>
  </div>
  <div v-if="showLoadingModal" class="modal-overlay">
    <div class="loading-modal-content">
      <div class="spinner"></div>
      <p>Applying contributions, please wait...</p>
    </div>
  </div>


</template>

<script>
import axios from 'axios';

export default {
  name: "UnitDevelopment",
  data() {
    return {
      showLoadingModal: false,
      library: [],
      sketches: [],
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
      solutions: {},
      images: [],
      showSlider: false, 
      hue: 0, 
      selectedColor: "FFFFFF", 
      undoStack: [], 
      redoStack: [],
      transparency: 127,
      value: 0,
      motion: 0,
      scale: 200,
      concentration: 127,
      space: 254,
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
      hoveredInfo: null
    };
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
    const searchedTerm = this.$route.query.searchedTerm ? JSON.parse(this.$route.query.searchedTerm) : '';
    const semanticSearch = this.$route.query.semanticSearch ? JSON.parse(this.$route.query.semanticSearch) : [];
    const library = this.$route.query.png_files ? JSON.parse(this.$route.query.png_files) : [];
    const info_library = this.$route.query.png_files_name ? JSON.parse(this.$route.query.png_files_name) : [];
    const decomposed_info = this.$route.query.decomposed_info ? JSON.parse(this.$route.query.decomposed_info) : [];
    this.searchedTerm = searchedTerm;
    this.semanticSearch = semanticSearch;
    this.library = library;
    this.decomposed_info = decomposed_info;
    this.library_names = info_library;
    
    this.points = [
        { x: this.value, y: this.transparency }, 
        { x: this.motion, y: this.scale },       
        { x: this.space, y: this.concentration } 
      ];
      
    fetch("http://127.0.0.1:5000/api/initial-solutions")
    .then((response) => response.json())
    .then((data) => {
      this.solutions = data.solutions;
      this.transparency = this.mapValue(data.solutions.principles.transparency, 0, 100, 0, 127); 
      this.value = this.mapValue(data.solutions.principles.value, 0, 100, 0, 127); 
      this.motion = this.mapValue(data.solutions.principles.motion, 0, 100, 127, 0); 
      this.scale = this.mapValue(data.solutions.principles.scale, 0, 100, 127, 252); 
      this.concentration = this.mapValue(data.solutions.principles.concentration, 0, 100, 127, 0); 
      this.space = this.mapValue(data.solutions.principles.space, 0, 100, 127, 254); 
      this.startSystem();
    })
    .catch((error) => console.error("Error fetching initial solutions:", error));

  },
  methods: {
    async loadImages() {

      this.previousStates= [];
      this.newState= [];
      this.firstLoad = true;
      this.images = []; 


      this.message = "";
      this.angle_value = 0;
      this.angle_space = 0;
      this.messagesToShow = [];
      this.interacting = false;

      const imagePaths = this.solutions.src.map(index => `/static/elements_png/${index}.png`);
      const imagePromises = imagePaths.map(path => {
          return new Promise((resolve, reject) => {
              const img = new Image();
              img.src = path;
              img.onload = () => {
                  this.images.push({
                      image: img,
                      src: img.src,
                      x: 0, 
                      y: 50,
                      width: img.width,
                      height: img.height,
                      originalWidth: img.width,
                      originalHeight: img.height,
                      rotation: 0,
                      opacity: 1,
                      backgroundColor: this.selectedColor
                  });
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
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext("2d");

        if (!canvas) {
            console.error("Canvas element not found!");
            return;
        } 

        if (!ctx) {
            console.error("Failed to get 2D context");
            return;
        } else {
          ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); 
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
        return;
      }

      let remainingOpacity = averageOpacity * imageCount; 
      this.images.forEach((image, index) => {
        if (index === imageCount - 1) {
          image.opacity = Math.max(0, Math.min(remainingOpacity, 1));
        } else {
          const maxPossible = Math.min(1, remainingOpacity - (imageCount - index - 1) * 0.2);
          const minPossible = Math.max(0.2, remainingOpacity - (imageCount - index - 1) * 1);
          image.opacity = Math.random() * (maxPossible - minPossible) + minPossible;
          remainingOpacity -= image.opacity;
        }
      });
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

      const requiredTotalDeviation = targetAverageDeviation * this.images.length;

      let currentTotalDeviation = 0;
      const deviations = []; 

      this.images.forEach((image) => {
        const randomFactor = Math.random(); 
        const initialDeviation = targetAverageDeviation * randomFactor * maxRotation;

        image.rotation = Math.random() < 0.5 ? -initialDeviation : initialDeviation;

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
        currentTotalDeviation = 0; 

        this.images.forEach((image, index) => {

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
      const maxDifference = 1; 
      const minScale = 127;    
      const maxScale = 252;   

      const targetAverageDifference = this.mapValue(
        targetScale,
        maxScale,
        minScale,
        0, 
        maxDifference 
      );

      if (targetScale === 254) {
        this.images.forEach((image) => {
          image.width = image.originalWidth;
          image.height = image.originalHeight;
        });
        return;
      }

      if (this.images.length < 2) {
        console.error("Not enough images for inverse mapping scale.");
        return;
      }

      this.images.forEach((image) => {
        image.width = image.originalWidth;
        image.height = image.originalHeight;
      });

      const adjustmentStep = 1; 
      let iteration = 0;
      let currentAverageDifference = 0;

      while (iteration < 1500) {
        iteration++;
        let totalRelativeDifference = 0;
        let pairCount = 0;

        for (let i = 0; i < this.images.length; i++) {
          for (let j = i + 1; j < this.images.length; j++) {
            const imgA = this.images[i];
            const imgB = this.images[j];

            const originalRatio = imgA.originalWidth / imgB.originalWidth;

            const currentRatio = imgA.width / imgB.width;

            const relativeDifference = Math.abs(Math.log(currentRatio / originalRatio));

            totalRelativeDifference += relativeDifference;
            pairCount++;

            if (relativeDifference < targetAverageDifference) {
              imgA.width += adjustmentStep;
              imgA.height = imgA.width * (imgA.originalHeight / imgA.originalWidth);
            } else {
              imgA.width -= adjustmentStep;
              imgA.height = imgA.width * (imgA.originalHeight / imgA.originalWidth);
              
            }
          }
        }

        currentAverageDifference = totalRelativeDifference / pairCount;
        
        if (Math.abs(currentAverageDifference - targetAverageDifference) < 0.001) {
          break;
        }
      }

      this.images.forEach((image) => {
        if (image.width > 300) {
          image.width = 300;
          image.height = image.width * (image.originalHeight / image.originalWidth); 
        }
        if (image.height > 300) {
          image.height = 300;
          image.width = image.height * (image.originalWidth / image.originalHeight); 
        }
        image.width = Math.max(image.width, 1);
        image.height = Math.max(image.height, 1);
      });
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

      const minThreshold = 60;
      const maxThreshold = Math.min(canvas.width, canvas.height) * 0.5;
      const mappedMin = 127, mappedMax = 0;

      const targetAverageDistance = this.mapValue(
        targetConcentration, mappedMin, mappedMax, minThreshold, maxThreshold
      );

      const elementRadius = Math.min(...this.images.map(img => Math.max(img.width, img.height))) / 2;
      const positions = [];
      let attempts = 0;
      let maxAttempts = 1000;

      while (positions.length < this.images.length && attempts++ < maxAttempts) {
        const candidate = {
          x: Math.random() * (canvas.width - 2 * elementRadius) + elementRadius,
          y: Math.random() * (canvas.height - 2 * elementRadius) + elementRadius,
        };

        if (positions.every(pos => {
          const dx = pos.x - candidate.x, dy = pos.y - candidate.y;
          return Math.abs(Math.sqrt(dx * dx + dy * dy) - targetAverageDistance) >= minThreshold;
        })) {
          positions.push(candidate);
        }
      }

      if (positions.length !== this.images.length) {
        console.warn("Retrying with adjusted thresholds...");
        maxAttempts += 500;
        this.inverseMappingConcentration(targetConcentration);
        return;
      }


      this.images.forEach((image, index) => {
        image.x = positions[index].x - image.width / 2;
        image.y = positions[index].y - image.height / 2;
        this.ensureWithinCanvas(image, canvas);
      });

      this.concentration = targetConcentration;
      this.updatePoints();
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

        if (image.width < 50) {
          const aspectRatio = image.height / image.width; 
          image.width = 50;
          image.height = image.width * aspectRatio;
        }
        if (image.height < 50) {
          const aspectRatio = image.width / image.height; 
          image.height = 50;
          image.width = image.height * aspectRatio;
        }
        this.ensureWithinCanvas(image, canvas);

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
        console.error("Error: 'images' is not an array or it's undefined.");
        return [];
      }

      return this.images.map(imageObj => ({
        ...imageObj,
        image: imageObj.image,
      }));
    },

    cloneCanvasStateManual() {
      return JSON.parse(JSON.stringify(this.images.map((image) => ({
        image: image,
        src: image.src,
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
            console.error("Invalid background color");
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
                console.error("Image invalid:", imageObj);
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

      const focusRadius = 60; 
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
        } else {
          score += 0;
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
        }else {
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
      this.previousStates = JSON.parse(JSON.stringify(this.cloneCanvasState()));
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
      if (this.areStatesDifferent(this.previousStates, this.newState)) {
        this.saveState();

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
        this.drawImages(ctx);
        this.transparency = this.mappingTransparency();
        this.updatePoints();
        this.newState = this.cloneCanvasState(); 
      }


    },
    async finalizeTransparencyChange() {      
      if (this.areStatesDifferent(this.previousStates, this.newState)) {
        this.saveState();

        this.interacting = true;
        this.images = await this.generateAndSelectBestSolution();
        this.drawSuggestions();
        this.interacting = false;
      }
    },


    toggleSlider() {
      this.showSlider = !this.showSlider; 
    },

    /* ---------------------------------------------------------------------------------------------------- CANVAS TO VISUALIZATION */
    mappingScale() {
      let totalRelativeDifference = 0;
      let pairCount = 0;

      for (let i = 0; i < this.images.length; i++) {
        for (let j = i + 1; j < this.images.length; j++) {
          const imgA = this.images[i];
          const imgB = this.images[j];

          const originalRatio = imgA.originalWidth / imgB.originalWidth;

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
      const minThreshold = 60; 
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

      const proximityRatio = totalPairs > 0 ? closePairs / totalPairs : 0;

      let mappedConcentration = this.mapValue(
        proximityRatio, 
        0, 
        1, 
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
      
      const minSpace = 127;
      const maxSpace = 253;
      let mappedSpace = this.mapValue(
        emptySpaceScore,
        0,
        0.85,
        minSpace,
        maxSpace
      );
      if (mappedSpace > maxSpace){
        mappedSpace = maxSpace;
      } else if (mappedSpace < minSpace){
        mappedSpace = minSpace;
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
      try {
      this.showLoadingModal = true;
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
      } catch (error) {
        console.error("Error applying contributions:", error);
      } finally {
        this.showLoadingModal = false;
      }
    },

    /* ---------------------------------------------------------------------------------------------------- SYSTEM CONTRIBUTIONS */
    contributingElements() {
      if (!this.images.length || !this.library.length) {
        console.error("Images or library is empty!");
        return;
      }

      const randomImageIndex = Math.floor(Math.random() * this.images.length);
      const currentImageObj = this.images[randomImageIndex];
      const currentImageSrc = currentImageObj.image.src;

      let newImagePath;
      let newImageIndex;
      do {
        newImageIndex = Math.floor(Math.random() * this.library.length);
        newImagePath = this.library[newImageIndex];
      } while (newImagePath === currentImageSrc);

      const newImage = new Image();
      newImage.src = newImagePath;

      newImage.onload = async () => {
        const originalWidth = newImage.width;
        const originalHeight = newImage.height;
        const aspectRatio = newImage.height / newImage.width;
        const newWidth = currentImageObj.width;
        const newHeight = newWidth * aspectRatio;
       

        this.images[randomImageIndex] = {
          ...currentImageObj,
          image: newImage,
          src: newImagePath,
          width: newWidth,
          height: newHeight,
          originalWidth: originalWidth,
          originalHeight: originalHeight,
        };

        const normalizedCurrentImagePath = currentImageSrc.replace(window.location.origin, "").replace(/^\//, "");
        const normalizedLibrary = this.library.map(item => item.replace(window.location.origin, "").replace(/^\//, ""));

        const oldLibraryIndex = normalizedLibrary.findIndex(item => item === normalizedCurrentImagePath);
        const newLibraryIndex = normalizedLibrary.findIndex(item => item === newImagePath.replace(window.location.origin, "").replace(/^\//, ""));

        if (oldLibraryIndex !== -1 && newLibraryIndex !== -1 && Array.isArray(this.solutions.src)) {
          const solutionIndex = this.solutions.src.indexOf(oldLibraryIndex);
          if (solutionIndex !== -1) {
            this.solutions.src[solutionIndex] = newLibraryIndex;
          }
        }

        const message = {
          text: `<img style="padding: 2%" src="${currentImageSrc}" alt="Old Image"> ▶ <img style="padding: 2%" src="${newImagePath}" alt="New Image">`,
        };
        this.messagesToShow.push(message);

        this.newState = this.cloneCanvasState();
        this.interacting = true;

        this.images = await this.generateAndSelectBestSolution();
        const ctx = this.$refs.canvas.getContext("2d");
        this.drawImages(ctx);

        this.drawSuggestions();
        this.updatePoints();

        this.interacting = false;
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
                return "Decreasing the hue allows the background to be emphasised when the concentration is high.";

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
                    return "Increasing the movement introduces visual dynamics that complement the elevated negative space.";
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
                    return "Increasing the scale emphasises the elements even more.";
                }
            },
            {
                condition: () => this.scale >= 190 && this.value === 0,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.scale = Math.max(127, this.scale - increment);
                    return "Decreasing the scale compensates for the neutrality of the background, increasing the definition of the elements.";
                }
            },
            {
                condition: () => this.scale < 190 && this.value > 0,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.scale = Math.min(254, this.scale + increment);
                    return "Increasing the scale allows you to move the elements away from their original format, in a composition where the background is important.";
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
                    return "Increasing the scale allows you to move the elements closer to their original format.";
                }
            },
            {
                condition: () => this.scale >= 190 && this.space < 190,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.scale = Math.max(127, this.scale - increment);
                    return "Decreasing the scale makes it possible to increase the overall scale of the elements, emphasising the departure from their original format.";
                }
            },
            {
                condition: () => this.scale < 190 && this.space >= 190,
                action: () => {
                    increment = Math.floor(Math.random() * (0 - actualValue + 1)) + actualValue;    
                    this.scale = Math.min(254, this.scale + increment);
                    return "Increasing the scale makes it possible to reduce the overall scale of the elements, emphasising their proximity to their original format.";
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
                    return "Increasing the scale allows you to move elements away from their original format by overlapping them.";
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

   /* ---------------------------------------------------------------------------------------------------- INTERACTION */
    startInteraction(event) {
      this.previousStates = this.cloneCanvasState();
      const { offsetX, offsetY } = event;

      if (this.selectedItem !== null) {
        const selectedImage = this.images[this.selectedItem];
        this.activeHandle = this.getHandleUnderCursor(event, selectedImage);

        if (this.activeHandle) {
          return; 
        }
      }

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

      if (this.selectedItem !== null && this.images[this.selectedItem]) {
        const { offsetX, offsetY } = event;
        const imageObj = this.images[this.selectedItem];

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

            this.scale = this.mappingScale();
            this.space = this.mappingSpace();
            this.updatePoints();
          } else if (this.activeHandle.type === "rotate") {
            const centerX = imageObj.x + imageObj.width / 2;
            const centerY = imageObj.y + imageObj.height / 2;
            imageObj.rotation = Math.atan2(offsetY - centerY, offsetX - centerX);

            this.motion = this.mappingMotion();
            this.updatePoints();
          }
        } else if (this.dragging) {
          imageObj.x = offsetX - this.dragging.offsetX;
          imageObj.y = offsetY - this.dragging.offsetY;

          this.concentration = this.mappingConcentration();
          this.space = this.mappingSpace();
          this.updatePoints();
        }

        const ctx = this.$refs.canvas.getContext("2d");
        this.drawImages(ctx);
      }
    },

    async stopInteraction() {
      this.dragging = null;
      this.activeHandle = null;

      this.newState = this.cloneCanvasState();

      if (this.areStatesDifferent(this.previousStates, this.newState) && this.firstLoad === false) {
          this.saveState(); 
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

    areStatesDifferent(stateA, stateB) {
      if (!Array.isArray(stateA) || !Array.isArray(stateB)) {
        return stateA !== stateB;
      }

      if (stateA.length !== stateB.length) {
        return true;
      }

      for (let i = 0; i < stateA.length; i++) {
        const imgA = stateA[i];
        const imgB = stateB[i];

        if (!imgA || !imgB) return true;

        if (
          imgA.src !== imgB.src || 
          imgA.x !== imgB.x ||
          imgA.y !== imgB.y ||
          imgA.width !== imgB.width ||
          imgA.height !== imgB.height ||
          imgA.rotation !== imgB.rotation ||
          imgA.opacity !== imgB.opacity ||
          imgA.backgroundColor !== imgB.backgroundColor
        ) {
          return true; 
        }
      }

      return false;
    },


    /* ---------------------------------------------------------------------------------------------------- SYSTEM SUGGESTIONS */
    drawSuggestions() {
      this.suggestions.forEach((suggestion, index) => {
        const canvas = this.$refs[`suggestionCanvas${index}`][0];
        if (!canvas) {
          console.error(`Canvas for suggestion ${index} not found.`);
          return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          console.error(`Context for suggestion ${index} not found.`);
          return;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        suggestion.forEach((imageObj) => {
          const { image, x, y, width, height, rotation, opacity } = imageObj;

          if (!image) {
            console.warn("Invalid images in a suggestion:", imageObj);
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
      if (!this.solutions || !Array.isArray(this.solutions.src)) {
        return false;
      }

      const imageIndex = this.library.findIndex(item => item === imageSrc);

      return this.solutions.src.includes(imageIndex);
    },

    async toggleSelection(imageSrc) {
        const imageIndex = this.library.findIndex(item => item === imageSrc);
        if (!this.solutions || !Array.isArray(this.solutions.src)) {
          return;
        }

        const canvas = this.$refs.canvas;
        const ctx = canvas.getContext("2d");

        if (this.solutions.src.includes(imageIndex)) {
            this.solutions.src = this.solutions.src.filter(index => index !== imageIndex);

            const targetSrc = `http://127.0.0.1:5000/static/elements_png/${imageIndex}.png`;
            this.images = this.images.filter(item => item.src !== targetSrc);


            if (this.selectedItem === imageIndex) {
                this.selectedItem = null; 
            } else if (this.selectedItem > imageIndex) {
                this.selectedItem -= 1; 
            }
        } else {
            const elementRadius = this.images.length
                ? Math.min(...this.images.map(img => Math.max(img.width, img.height))) / 2
                : 50; 

            this.solutions.src.push(imageIndex);
            const imagePaths = [`/static/elements_png/${imageIndex}.png`];

            const imagePromises = imagePaths.map(path => {
                return new Promise((resolve, reject) => {
                    const img = new Image();
                    img.src = path;
                    img.onload = () => {
                        this.images.push({
                            image: img,
                            src: img.src,
                            x: Math.random() * (canvas.width - 2 * elementRadius) + elementRadius,
                            y: Math.random() * (canvas.height - 2 * elementRadius) + elementRadius,
                            width: img.width,
                            height: img.height,
                            originalWidth: img.width,
                            originalHeight: img.height,
                            rotation: 0,
                            opacity: 1,
                            backgroundColor: this.selectedColor,
                        });
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
            imagePath: `/static/InputWorks/${decomposedData.id_imagem}`,
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
    
    /* ---------------------------------------------------------------------------------------------------- USER TOOLS */
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
          console.error("Error in API:", error);
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
      });
    },


    drawSaved() {
  let color = "";
  
  this.sketches.forEach((sketch, index) => {
    const canvas = this.$refs[`sketchesCanvas${index}`][0];
    if (!canvas) {
      console.error(`Canvas for suggestion ${index} not found.`);
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      console.error(`Failed obtaining context for suggestion ${index}`);
      return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    sketch.forEach((imageObj) => {
      const { image, x, y, width, height, rotation, opacity, backgroundColor } = imageObj;
      color = backgroundColor;

      if (!(image instanceof HTMLImageElement)) {
        console.warn("Invalid image in sketch:", imageObj);
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

  const solutionsArray = this.solutions.src;

  this.sketches.forEach((sketchArray, arrayIndex) => {
    if (!Array.isArray(sketchArray)) {
      console.error(`Unexpected element in this.sketches at index ${arrayIndex}.`);
      return;
    }

    if (sketchArray.length === solutionsArray.length) {
      solutionsArray.forEach((src, index) => {
        if (sketchArray[index]) {
          if (typeof src === "string") {
            const img = new Image();
            img.src = src;
            sketchArray[index].image = img;
          }
        }
      });
    } else {
      console.error(`Arrays index: ${arrayIndex} - are not the same size`);
    }
  });
},



    pattern() {
        if (this.sketches.length === 0) {
            alert("You need to save a sketch before proceeding with the development of the pattern.");
            return;
        }
        this.exportAllCanvases();
    },

    async exportAllCanvases() {
      const uploadPromises = this.sketches.map((_, index) => {
        const canvasRef = this.$refs[`sketchesCanvas${index}`];
        const canvas = Array.isArray(canvasRef) ? canvasRef[0] : canvasRef;

        if (!canvas) {
          console.error(`Canvas ${index} not found!`);
          return Promise.resolve(); 
        }

        const dataURL = canvas.toDataURL("image/png");

        return axios.post("http://127.0.0.1:5000/api/save_canvas", {
            imageData: dataURL,
            fileName: `sketch_${index}.png`,
          })
          .catch(err => console.error(`Erro no sketch_${index}:`, err));
      });

      try {        
        await Promise.all(uploadPromises);
        await new Promise(resolve => setTimeout(resolve, 500));

        this.$router.push({ 
          name: 'PatternDevelopment', 
          query: { sketches: JSON.stringify(this.sketches) } 
        });

      } catch (error) {
        console.error("Critical error in the export process:", error);
      }
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

.library-item {
  width: 98%;
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

.change-section .check-mark.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.changeImage{
  width: 10%;
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

.images-container {
  max-height: 95%;
  overflow-y: auto;
  overflow-x: hidden;
}

.images-container-left{
  padding-right: 1rem;
  max-height: 100%; 
  overflow-y: auto;
  overflow-x: hidden;
}

.images-container::-webkit-scrollbar {
  width: 0.5rem;
  border-radius: 20px;
}
.images-container::-webkit-scrollbar-thumb {
  background-color: #A67E66;
  border-radius: 20px;
}
.images-container::-webkit-scrollbar-track {
  background: #efe3d1;
  border-radius: 20px;
}
</style>
