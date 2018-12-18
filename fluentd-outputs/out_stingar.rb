require "uri"
require "json"
require "httpclient"
require "fluent/plugin/output"


class Fluent::Plugin::CIFOutput < Fluent::Plugin::Output
    Fluent::Plugin.register_output('cif', self)

    config_param :cif_host, :string
    config_param :cif_token, :string, default: nil, secret: true

    config_param :cif_provider, :string, default: "chn"
    config_param :cif_tlp, :string, default: "green"
    config_param :cif_confidence, :integer, default: 8
    config_param :cif_tags, :array, default: ["honeypot"]
    config_param :cif_group, :string, default: "everyone"
    config_param :cif_default, :string, default: "green"

    def initialize
        super
    end

    def configure(conf)
        super

        @handle = HTTPClient.new(:agent_name => 'fluentd-cif')
        @uri = URI.parse("#{@cif_host}/indicators")
        @headers = {'Authorization'=> "Token token=#{@cif_token}",
                    'Content-Type' => "application/json"}
    end

    def process(tag, es)
        es.each do |_time, record|
            indicator = {
                "indicator"   => record['src_ip'],
                "tlp"         => @cif_tlp,
                "provider"    => @cif_provider,
                "group"       => @cif_group,
                "tags"        => @cif_tags + [record['app']],
                "confidence"  => @cif_confidence
            }
            submit(indicator)
        end
    end

    def submit(indicator)
        data = JSON.generate(indicator)
        puts(data)
        @handle.post(@uri, data, headers=@headers)
    end
end