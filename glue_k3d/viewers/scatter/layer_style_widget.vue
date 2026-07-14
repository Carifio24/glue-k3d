<template>
    <div class="glue-layer-scatter">
        <div class="text-subtitle-2 font-weight-bold">Color</div>
        <div>
            <v-select label="color" :items="cmap_mode_items" v-model="cmap_mode_selected" hide-details />
        </div>
        <template v-if="(cmap_mode_items[cmap_mode_selected] || {}).text === 'Linear'">
            <div>
                <v-select label="attribute" :items="cmap_att_items" v-model="cmap_att_selected" hide-details />
            </div>
            <div>
                <glue-float-field label="min" :value.sync="cmap_vmin" echo-type="float" />
            </div>
            <div>
                <glue-float-field label="max" :value.sync="cmap_vmax" echo-type="float" />
            </div>
            <div>
                <v-select label="colormap" :items="cmap_items" v-model="cmap" hide-details />
            </div>
        </template>
        <div>
            <v-subheader class="pl-0 slider-label">opacity</v-subheader>
            <glue-throttled-slider wait="300" min="0" max="1" step="0.01" :value.sync="alpha" echo-type="float" hide-details />
        </div>
        <div>
            <v-select label="shader" :items="shader_items" v-model="shader_selected" />
        </div>
        <div class="text-subtitle-2 font-weight-bold">Points</div>
        <v-select label="size" :items="size_mode_items" v-model="size_mode_selected" hide-details />
        <template v-if="(size_mode_items[size_mode_selected] || {}).text === 'Linear'">
            <div>
                <v-select label="attribute" :items="size_att_items" v-model="size_att_selected" hide-details />
            </div>
            <div>
                <glue-float-field label="min" :value.sync="size_vmin" echo-type="float" />
            </div>
            <div>
                <glue-float-field label="max" :value.sync="size_vmax" echo-type="float" />
            </div>
        </template>
        <template v-else>
            <div>
                <glue-float-field label="size" :value.sync="size" echo-type="int" />
            </div>
        </template>
        <div>
            <v-subheader class="pl-0 slider-label">size scaling</v-subheader>
            <glue-throttled-slider wait="300" min="0.1" max="10" step="0.01" :value.sync="size_scaling" echo-type="float"
                hide-details />
        </div>
    </div>
</template>

<style id="layer_scatter">
.glue-layer-scatter .v-subheader.slider-label {
    font-size: 12px;
    height: 16px;
    margin-top: 6px;
}
</style>
