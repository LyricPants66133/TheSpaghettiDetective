<template>
<div class="row justify-content-center">
  <pull-to-reveal>
    <navbar view-name="app.views.web_views.edit_printer"></navbar>
  </pull-to-reveal>

  <div class="col-sm-12 col-lg-10 wizard-container form-container">
    <div v-if="verifiedPrinter" class="text-center py-5">
      <img
        :src="require('../../../app/static/img/checkmark.png')" />
      <h2>{{verifiedPrinter.name}}</h2>
      <div class="lead">Successfully linked to your account!</div>
      <br /><br />
      <div class="col-sm-12 col-md-8 offset-md-2 col-lg-6 offset-lg-3 d-flex flex-column align-center justify-content-center">
        <div class="mt-4">
          <a href="/printers/" class="btn-primary btn-block mx-auto btn btn-lg">Go Check Out Printer Feed!</a>
        </div>
        <div class="mt-5">
          <a href="/user_preferences/" class="btn btn-outline-secondary btn-block mx-auto btn">Add Phone Number</a>
        </div>
        <div>
          <div class="text-muted mx-auto text-center font-weight-light">So that The Detective can send you text (SMS) on print failures.</div>
        </div>
        <div class="mt-4">
          <a :href="editPrinterUrl" class="btn btn-outline-secondary btn-block mx-auto btn">Change Printer Settings</a>
        </div>
        <div>
          <div class="text-muted mx-auto text-center font-weight-light">You can always change it later.</div>
        </div>
      </div>
    </div>
    <div v-else>
      <form-wizard
        :color="theme.primary"
        step-size="sm"
      >
        <h2 slot="title">
          <img class="header-img"
            :src="require('../../../app/static/img/octo-inverted.png')" />
          {{title}}
        </h2>
        <tab-content v-if="printerIdToLink" title="Open Plugin Settings">
          <div class="container">
            <div class="row justify-content-center pb-3">
              <div class="col-sm-12 col-lg-8">
                <div class="text-warning">
                  Warning: Re-Linking OctoPrint should be your last resort to solve issues. Please make sure you have exhausted all options on <a href="https://www.thespaghettidetective.com/help/">TSD's help website</a>.
                </div>
                <ol>
                  <li>Open OctoPrint in another browser tab. </li>
                  <li>Select <em>"OctoPrint settings menu → Access Anywhere - The Spaghetti Detective"</em>.</li>
                  <li>Select <em>"Troubleshooting → Re-run Wizard"</em>.</li>
                </ol>
              </div>
            </div>
            <div class="row justify-content-center">
              <div class="col-sm-12 col-lg-8 img-container">
                <img class="mx-auto" :src="require('@static/img/plugin_rerun_setup.png')">
              </div>
            </div>
          </div>
        </tab-content>
        <tab-content v-else title="Install Plugin">
          <div class="container">
            <div class="row justify-content-center pb-3">
              <div class="col-sm-12 col-lg-8">
                <ol>
                  <li>Open OctoPrint in another browser tab. </li>
                  <li>Select <em>"OctoPrint settings menu → Plugin Manager → Get More..."</em>.</li>
                  <li>Enter "The Spaghetti Detective" to locate the plugin. Click <em>"Install"</em>.</li>
                  <li>Restart OctoPrint when prompted.</li>
                </ol>
              </div>
            </div>
            <div class="row justify-content-center">
              <div class="col-sm-12 col-lg-8 img-container">
                <img
                  class="mx-auto screenshot"
                  :src="require('@static/img/install_plugin.png')"
                  @click="zoomIn($event)">
              </div>
            </div>
          </div>
        </tab-content>
        <tab-content title="Plugin Wizard">
          <div class="container">
            <div class="row justify-content-center pb-3">
              <div class="col-sm-12 col-lg-8">
                <ol>
                  <li>Wait for <em>"Access Anywhere - The Spaghetti Detective"</em> wizard to popup.</li>
                  <li>Follow the instructions in the wizard.</li>
                  <li>Select <em>"Web Setup"</em> when asked.</li>
                </ol>
              </div>
            </div>
            <div class="row justify-content-center">
              <div class="col-sm-12 col-lg-8 img-container">
                <img
                  class="mx-auto screenshot"
                  :src="require('@static/img/plugin_wizard_websetup.png')"
                  @click="zoomIn($event)">
              </div>
            </div>
          </div>
        </tab-content>
        <tab-content title="Enter Code">
          <div class="container">
            <div class="row justify-content-center pb-3">
              <div class="col-sm-12 col-lg-8  d-flex flex-column align-items-center">
                  <input disabled ref="code" class="code-btn" :value="`${verificationCode && verificationCode.code}`"/>
                  <small class="mx-auto py-1" :class="{'text-muted': !copied}">{{ copied ? 'Code copied to system clipboard' : 'Ctrl-C/Cmd-C to copy the code'}}</small>
                  <div class="mx-auto pt-1 pb-4"><span class="text-muted">Code expires in </span>{{timeToExpire}}</div>
                <div class="lead">Enter the <strong>6-digit verification code</strong> in the plugin</div>
              </div>
            </div>
            <div class="row justify-content-center">
              <div class="col-sm-12 col-lg-8 img-container">
                <img
                  class="screenshot"
                  :src="require('@static/img/plugin_verification_code.png')"
                  @click="zoomIn($event)">
                <div class="helper mx-auto py-2"><a class="link font-weight-bold" @click="showVerificationCodeHelpModal">Can't find the page to enter the 6-digit code?</a></div>
              </div>
            </div>
          </div>
        </tab-content>

        <template slot="footer" slot-scope="props">
          <div class="wizard-footer-left">
            <wizard-button v-if="props.activeTabIndex > 0" @click.native="props.prevTab(); prevTab();" class="btn btn-link btn-back">&lt; Back</wizard-button>
          </div>
          <div class="wizard-footer-right">
            <wizard-button v-if="!props.isLastStep" @click.native="props.nextTab(); nextTab();" class="wizard-footer-right wizard-btn" :style="props.fillButtonStyle">Next &gt;</wizard-button>
          </div>
        </template>
      </form-wizard>
      <div class="row">
        <div class="helper col-sm-12">Need help? Check out the <a href="https://help.thespaghettidetective.com/kb/guide/en/setup-the-spaghetti-detective-using-the-web-app-dbCcgiR0Tr/">step-by-step set up guide.</a></div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
import urls from '@lib/server_urls'
import {WizardButton, FormWizard, TabContent} from 'vue-form-wizard'
import 'vue-form-wizard/dist/vue-form-wizard.min.css'
import theme from '../main/main.sass'
import PullToReveal from '@common/PullToReveal.vue'
import Navbar from '@common/Navbar.vue'

export default {
  components: {
    FormWizard,
    TabContent,
    WizardButton,
    PullToReveal,
    Navbar,
  },
  data() {
    return {
      theme: theme,
      verificationCode: null,
      verifiedPrinter: null,
      onVerificationStep: false,
      copied: false
    }
  },

  computed: {
    printerIdToLink() {
      return new URLSearchParams(window.location.search.substring(1)).get('printerId')
    },
    title() {
      return this.printerIdToLink ? 'Re-Link OctoPrint' : 'Link OctoPrint'
    },
    editPrinterUrl() {
      return `/printers/${this.verifiedPrinter.id}/`
    },
    expiryMoment() {
      if (this.verificationCode) {
        return moment(this.verificationCode.expired_at)
      } else {
        return null
      }
    },
    timeToExpire() {
      if (this.expiryMoment) {
        return moment.duration(this.expiryMoment.diff(moment())).humanize()
      } else {
        return '-'
      }
    }
  },
  methods: {
    /**
     * Functions prevTab() and nextTab() are used to remove .checked class from circle steps
     * following current step (.checked class isn't removed by default after clicking Back
     * button, which causes showiing logo inside furter steps, not only completed ones).
     */
    prevTab() {
      document.querySelector('.wizard-nav.wizard-nav-pills li.active .wizard-icon-circle').classList.remove('checked')
      this.onVerificationStep = document.querySelector('.wizard-nav.wizard-nav-pills li.active .wizard-icon-circle').id === 'step-PluginWizard1'
    },
    nextTab() {
      document.querySelector('.wizard-nav.wizard-nav-pills li.active .wizard-icon-circle').classList.add('checked')

      this.onVerificationStep = document.querySelector('.wizard-nav.wizard-nav-pills li.active .wizard-icon-circle').id === 'step-PluginWizard1'

      if (this.onVerificationStep) {
        if (!this.codeInterval) {
          this.getVerificationCode()

          this.codeInterval = setInterval(() => {
            this.getVerificationCode()
          }, 5000)
        }

        const copyFunc = this.copyCode

        let ctrlDown = false, ctrlKey = 17, cmdKey = 91, cKey = 67

        document.addEventListener('keydown', function(e) {
          if (e.keyCode == ctrlKey || e.keyCode == cmdKey) ctrlDown = true
        })
        document.addEventListener('keyup', function(e) {
          if (e.keyCode == ctrlKey || e.keyCode == cmdKey) ctrlDown = false
        })

        document.addEventListener('keydown', function(e) {
          if (ctrlDown && (e.keyCode == cKey)) {
            copyFunc()
          }
        })
      }
    },
    url() {
      const baseUrl = urls.verificationCode()
      if (!this.verificationCode){ // Never retrieved veification code. Get one.
        if (this.printerIdToLink) {
          return `${baseUrl}?printer_id=${this.printerIdToLink}`
        } else {
          return baseUrl
        }
      }

      if (this.verificationCode.verified_at) { // Code is verified successfully, keep on polling to get update on the printer name if any
        return `${baseUrl}${this.verificationCode.id}/`
      }

      if (moment().isBefore(this.expiryMoment)) { // Not verified, and not expired
        return `${baseUrl}${this.verificationCode.id}/`
      }

      // Not verified, but expired.
      return baseUrl
    },
    /**
     * Copy verification code to clipboard (on appropriate step)
     */
    copyCode() {
      if (this.onVerificationStep) {
        let textArea = document.createElement('textarea')
        textArea.value = this.verificationCode.code

        // Avoid scrolling to bottom
        textArea.style.top = '0'
        textArea.style.left = '0'
        textArea.style.position = 'fixed'

        document.body.appendChild(textArea)
        textArea.focus()
        textArea.select()

        try {
          document.execCommand('copy')
          this.copied = true
        } catch (err) {
          console.error('Fallback: Oops, unable to copy', err)
        }

        document.body.removeChild(textArea)
      }
    },

    /**
     * Get verification code from API
     */
    getVerificationCode() {
      axios
        .get(this.url())
        .then((resp) => {
          if (resp.data) {
            if (resp.data) {
              this.verificationCode = resp.data
              if (this.verificationCode.verified_at) {
                this.verifiedPrinter = resp.data.printer
              }
            }
          }
        })
    },

    showVerificationCodeHelpModal() {
      this.$swal.fire({
        title: 'Can\'t find the page to enter the 6-digit code?',
        html: `<p>The 6-digit code needs to be entered in The Spaghetti Detective plugin in OctoPrint. There are a few reasons why you can't find this page:</p>
        <p><ul>
        <li style="margin: 10px 0;">You don't have the plugin installed or you haven't restarted OctoPrint after installation. Click <a href="/printers/wizard/">here</a> to walk through the process again.</li>
        <li style="margin: 10px 0;">The installed plugin is on a version earlier than 1.5.0. You need to upgrade the plugin to <b>1.5.0</b> or later.</li>
        <li style="margin: 10px 0;">Still no dice? Check out the step-by-step <a href="https://help.thespaghettidetective.com/kb/guide/en/setup-the-spaghetti-detective-using-the-web-app-dbCcgiR0Tr/">set up guide</a>.</li>
        </ul></p>`,
        customClass: {
          container: 'dark-backdrop',
        },
      })
    },

    zoomIn(event) {
      event.target.classList.toggle('zoomedIn')
    },
  }
}
</script>

<style lang="sass" scoped>
@use "~main/theme"

.wizard-btn
  border-radius: 300px

.wizard-container
  padding: 1em
  background: theme.$body-bg
  -webkit-box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.3) !important
  box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.3) !important
  border: none !important

.btn-back
  color: theme.$white
  min-width: auto

.container
  padding: 0

.header-img
  width: 1em
  height: 1em
  margin-right: 12px
  margin-bottom: 8px

.img-container
  background: darken(theme.$body-bg, 5)
  padding: 1rem
  text-align: center

img
  max-height: 30vh

.spacer
 width: 200px

.code-btn
  border-radius: 10px
  text-align: center
  width: 21rem
  height: 60px
  background-color: black
  border: black
  color: white
  font-size: 2rem
  font-weight: 500
  letter-spacing: 0.5em

.helper
  text-align: center
  padding: 0 36px

li
  margin: 2px -35px

.screenshot
  max-width: 100%
  transition: transform .3s

  &:hover
    cursor: pointer

  &.zoomedIn
    transform: scale(2)
    position: relative
    z-index: 9
</style>

<style lang="sass">
// Unscoped styles to style plugin elements
@use "~main/theme"

// Step label (not active)
.wizard-container .vue-form-wizard .wizard-nav-pills > li:not(.active) > a > span
  color: theme.$white

// Adjust numbers in the circles (form steps)
.wizard-nav.wizard-nav-pills .wizard-icon-circle i
  position: relative
  right: 2px

// Show logo inside completed sorm step circles
.wizard-nav.wizard-nav-pills li:not(.active)
  .wizard-icon-circle.checked i
    display: none

  .wizard-icon-circle.checked:before
    $size: 30px
    content: ""
    display: block
    width: $size
    height: $size
    background-image: url("/static/img/logo-square.png")
    background-size: $size $size
    position: absolute
    top: calc(50% - #{$size / 2})
    left: calc(50% - #{$size / 2})
    bottom: calc(50% - #{$size / 2})
    right: calc(50% - #{$size / 2})
</style>
