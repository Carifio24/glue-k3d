<template>
    <div>
        <div>
            <v-select label="attribute" :items="attribute_items" v-model="attribute_selected" hide-details class="margin-bottom: 16px" />
        </div>
        <template v-if="(cmap_mode_items[cmap_mode_selected] || {}).text === 'Linear'">
          <div>
              <v-select label="colormap" :items="cmap_items" :value="cmap" @change="set_colormap" hide-details/>
          </div>
        </template>
        <div v-if="!subset">
            <v-select label="color" :items="cmap_mode_items" v-model="cmap_mode_selected" hide-details />
        </div>
        <div>
            <v-subheader class="pl-0 slider-label">opacity</v-subheader>
            <glue-throttled-slider wait="300" max="1" step="0.01" :value.sync="alpha" echo-type="float" hide-details />
        </div>
        <div>
            <glue-float-field label="min" :value.sync="vmin" echo-type="float" />
        </div>
        <div>
            <glue-float-field label="max" :value.sync="vmax" echo-type="float" />
        </div>
    </div>
</template>

<style id="layer_volume">
    .v-subheader.slider-label {
        font-size: 12px;
        height: 16px;
    }
</style>
