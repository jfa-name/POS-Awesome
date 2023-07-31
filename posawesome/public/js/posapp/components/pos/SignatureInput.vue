<template>
    <v-dialog v-model="signatureDialog" max-width="500px">
        <v-card>
            <v-card-title class="headline">Enter Signature</v-card-title>
            <v-card-text>
                <div ref="signatureContainer" style="width: 100%; height: 200px;"></div>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="error" @click="cancelSignature">Cancel</v-btn>
                <v-btn color="primary" @click="saveSignature">Save</v-btn>
                <v-btn color="caution" @click="clearSignature">Clear</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import SignaturePad from 'signature_pad';

export default {
    data() {
        return {
            signatureDialog: false,
            signaturePad: null,
        };
    },
    methods: {
        openSignatureDialog() {
            this.signatureDialog = true;
            // Initialize the signature pad when the dialog is opened
            this.$nextTick(() => {
                this.initializeSignaturePad();
            });
        },
        cancelSignature() {
            this.signatureDialog = false;
        },
        saveSignature() {
            if (this.signaturePad.isEmpty()) {
                alert('Please provide a signature before saving.');
                return;
            }

            const signatureDataURL = this.signaturePad.toDataURL();
            // Emit the signature data back to the parent component (Proceed.vue)
            this.$emit('signature-entered', signatureDataURL);
            this.signatureDialog = false;
        },
        initializeSignaturePad() {
            const container = this.$refs.signatureContainer;
            const canvas = document.createElement('canvas');
            container.appendChild(canvas);

            // Initialize the signature pad with the new canvas element
            this.signaturePad = new SignaturePad(canvas, {
                penColor: '#c0f',
            });
        },
        clearSignature() {
            this.signaturePad.clear(); // Clear the signature pad data
        },
    },
};
</script>
