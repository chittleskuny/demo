using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using YamlDotNet.RepresentationModel;

namespace Demo
{
    /// <summary>
    /// Yaml 文件读写器类。
    /// </summary>
    public class Yamler
    {
        /// <summary>
        /// 读文本。
        /// </summary>
        public static YamlMappingNode ReadText(string allText)
        {
            // Setup the input
            var input = new StringReader(allText);

            // Load the stream
            var yaml = new YamlStream();
            yaml.Load(input);

            // Examine the stream
            var root = (YamlMappingNode)yaml.Documents[0].RootNode;

            return root;
        }

        /// <summary>
        /// 读文件。
        /// </summary>
        public static YamlMappingNode Read(string filename)
        {
            var allText = File.ReadAllText(filename);
            return ReadText(allText);
        }

        /// <summary>
        /// 取 string 类型的值。
        /// </summary>
        public static string GetStringByKey(YamlMappingNode parent, string key)
        {
            return parent.Children[new YamlScalarNode(key)].ToString();
        }

        /// <summary>
        /// 取 int 类型的值。
        /// </summary>
        public static int GetIntByKey(YamlMappingNode parent, string key)
        {
            return int.Parse(parent.Children[new YamlScalarNode(key)].ToString());
        }

        /// <summary>
        /// 取 double 类型的值。
        /// </summary>
        public static double GetDoubleByKey(YamlMappingNode parent, string key)
        {
            return double.Parse(parent.Children[new YamlScalarNode(key)].ToString());
        }
    }
}
